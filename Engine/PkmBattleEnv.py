import gym
from gym import spaces
import random
import numpy as np
from typing import List, Tuple

from Engine.Competition.DeepEncoding import encode
from Engine.PkmBaseStructures import WeatherCondition, Pkm, PkmType, PkmStatus
from Engine.PkmConstants import N_SWITCHES, HIT_POINTS, N_MOVES, SPIKES_2, SPIKES_3, STATE_DAMAGE, N_TRAINERS, \
    TYPE_CHART_MULTIPLIER, N_PARTY


class PkmBattleEnv(gym.Env):
    def __init__(self, party_size: int = N_SWITCHES, debug: bool = False):

        # random active pokemon
        self.a_pkm = [Pkm(), Pkm()]
        # random party pokemon
        self.p_pkm = [[Pkm() for _ in range(party_size)], [Pkm() for _ in range(party_size)]]
        self.weather = WeatherCondition.CLEAR
        self.attack_stage = [0, 0]
        self.defense_stage = [0, 0]
        self.speed_stage = [0, 0]
        self.spikes = [0, 0]
        self.confused = [0, 0]
        self.n_turns_no_clear = 0
        self.n_turns_confused = [0, 0]
        self.switched = [False, False]
        self.debug = debug
        self.log = ''
        self.turn = 0
        self.party_size = party_size
        self.action_space = spaces.Discrete(N_MOVES + N_SWITCHES)
        self.observation_space = spaces.Discrete(len(encode(self._state_trainer(0))))

    def get_party_size(self):
        return self.party_size

    def step(self, actions):

        # Reset variables
        r = [0., 0.]
        t = [False, False]
        if self.debug:
            self.turn += 1
            self.log = 'TURN %s\n\n' % str(self.turn)

        # switch pkm
        self._process_switch_pkms(actions)

        # set trainer attack order
        first, second = self._get_attack_order()
        first_pkm = self.a_pkm[first]
        second_pkm = self.a_pkm[second]

        # get entry hazard damage
        dmg_2_first = self._get_entry_hazard_damage(first)
        dmg_2_second = self._get_entry_hazard_damage(second)

        r[first] = (dmg_2_second - dmg_2_first) / HIT_POINTS
        r[second] = (dmg_2_first - dmg_2_second) / HIT_POINTS

        active_not_fainted = not (first_pkm.fainted() or second_pkm.fainted())

        # process all pre battle effects
        self._process_pre_battle_effects()

        # confusion state damage
        dmg_2_first = self.__get_pre_combat_damage(first) if active_not_fainted else 0.
        dmg_2_second = self.__get_pre_combat_damage(second) if active_not_fainted else 0.

        confusion_damage_2_first = dmg_2_first > 0.
        confusion_damage_2_second = dmg_2_second > 0.

        r[first] += (dmg_2_second - dmg_2_first) / HIT_POINTS
        r[second] += (dmg_2_first - dmg_2_second) / HIT_POINTS

        active_not_fainted = not (first_pkm.fainted() or second_pkm.fainted())

        # battle
        first_can_attack = active_not_fainted and not self.a_pkm[first].paralyzed() and not self.a_pkm[
            first].asleep() and not confusion_damage_2_first
        dmg_2_second, hp_2_first = self._perform_pkm_attack(first, actions[first]) if first_can_attack else (0., 0.)

        active_not_fainted = not (first_pkm.fainted() or second_pkm.fainted())

        second_can_attack = active_not_fainted and not self.a_pkm[second].paralyzed() and not self.a_pkm[
            first].asleep() and not confusion_damage_2_second
        dmg_2_first, hp_2_second = self._perform_pkm_attack(second, actions[second]) if second_can_attack else (0., 0.)

        r[first] += (dmg_2_second + hp_2_first - dmg_2_first) / HIT_POINTS + float(second_pkm.fainted())
        r[second] += (dmg_2_first + hp_2_second - dmg_2_second) / HIT_POINTS + float(first_pkm.fainted())

        # get post battle effects damage
        dmg_2_first = self._get_post_battle_damage(first) if first_can_attack else 0.
        dmg_2_second = self._get_post_battle_damage(second) if second_can_attack else 0.

        r[first] += (dmg_2_second - dmg_2_first) / HIT_POINTS
        r[second] += (dmg_2_first - dmg_2_second) / HIT_POINTS

        # process all post battle effects
        self._process_post_battle_effects()

        # switch fainted pkm
        dmg_2_first, dmg_2_second = self.__switch_fainted_pkm()

        r[first] += (dmg_2_second - dmg_2_first) / HIT_POINTS
        r[second] += (dmg_2_first - dmg_2_second) / HIT_POINTS

        # check if battle ended
        t[first] = self._fainted_team(first)
        t[second] = self._fainted_team(second)

        r[first] += float(t[first])
        r[second] += float(t[second])

        return [self._state_trainer(0), self._state_trainer(1)], r, t[first] or t[second], None

    def enable_debug(self):
        self.debug = True

    def disable_debug(self):
        self.debug = False

    def _process_switch_pkms(self, actions: List[int]):
        """
        Switch pokemons if players chosen to do so

        :param actions: players actions
        :return:
        """
        if actions[0] >= N_MOVES:
            switch_action = actions[0] - N_MOVES
            if not self.p_pkm[0][switch_action].fainted():
                self._switch_pkm(0, switch_action)
        if actions[1] == N_MOVES:
            switch_action = actions[1] - N_MOVES
            if not self.p_pkm[1][switch_action].fainted():
                self._switch_pkm(1, switch_action)

    def _get_entry_hazard_damage(self, t_id: int) -> float:
        """
        Get triggered damage to be dealt to a switched pkm.

        :param: t_id: owner trainer
        :return: damage to first pkm, damage to second pkm
        """
        damage = 0.
        spikes = self.spikes[t_id]

        # Spikes damage
        if self.spikes[t_id] and self.a_pkm[t_id].type != PkmType.FLYING and self.switched[t_id]:
            pkm = self.a_pkm[t_id]
            before_hp = pkm.hp
            pkm.hp -= STATE_DAMAGE if spikes <= 1 else SPIKES_2 if spikes == 2 else SPIKES_3
            pkm.hp = 0. if pkm.hp < 0. else pkm.hp
            damage = before_hp - pkm.hp
            self.switched[t_id] = False
            if self.debug and damage > 0.:
                self.log += 'ENTRY HAZARD DAMAGE: %s takes %s entry hazard damage from spikes, hp reduces from %s to ' \
                            '%s\n' % (str(pkm), damage, before_hp, pkm.hp)

        return damage

    def _process_pre_battle_effects(self):
        """
        Process all pre battle effects.

        """
        # for all trainers
        for i in range(N_TRAINERS):

            pkm = self.a_pkm[i]

            # check if active pkm should be no more confused
            if self.confused[i]:
                self.n_turns_confused[i] += 1
                if random.uniform(0, 1) <= 0.5 or self.n_turns_confused[i] == 4:
                    self.confused[i] = False
                    self.n_turns_confused[i] = 0
                    if self.debug:
                        self.log += 'STATUS: Trainer %s\'s %s is no longer confused\n' % (i, str(pkm))

            # check if active pkm should be no more asleep
            if pkm.asleep():
                pkm.n_turns_asleep += 1
                if random.uniform(0, 1) <= 0.5 or pkm.n_turns_asleep == 4:
                    pkm.status = PkmStatus.NONE
                    pkm.n_turns_asleep = 0
                    if self.debug:
                        self.log += 'STATUS: Trainer %s\'s %s is no longer asleep\n' % (i, str(pkm))

    def _process_post_battle_effects(self):
        """
        Process all post battle effects.

        """
        if self.weather != WeatherCondition.CLEAR:
            self.n_turns_no_clear += 1

            # clear weather if appropriated
            if self.n_turns_no_clear > 5:
                self.weather = WeatherCondition.CLEAR
                self.n_turns_no_clear = 0
                if self.debug:
                    self.log += 'STATE: The weather is clear\n'

    def _get_post_battle_damage(self, t_id: int) -> float:
        """
        Get triggered damage to be dealt to switched pkm.

        :param: t_id: owner trainer
        :return: damage to pkm
        """
        pkm = self.a_pkm[t_id]
        state_damage = 0.

        if self.weather == WeatherCondition.SANDSTORM and (
                pkm.type != PkmType.ROCK and pkm.type != PkmType.GROUND and pkm.type != PkmType.STEEL):
            state_damage = STATE_DAMAGE
        elif self.weather == WeatherCondition.HAIL and (pkm.type != PkmType.ICE):
            state_damage = STATE_DAMAGE

        before_hp = pkm.hp
        pkm.hp -= state_damage
        pkm.hp = 0. if pkm.hp < 0. else pkm.hp
        damage = before_hp - pkm.hp

        if self.debug and state_damage > 0.:
            self.log += 'STATE DAMAGE: %s takes %s weather damage from sandstorm/hail hp reduces from %s to %s\n' % (
                str(pkm), damage, before_hp, pkm.hp)

        if pkm.status == PkmStatus.POISONED:
            state_damage = STATE_DAMAGE

            before_hp = pkm.hp
            pkm.hp -= state_damage
            pkm.hp = 0. if pkm.hp < 0. else pkm.hp
            damage = before_hp - pkm.hp

            if self.debug and damage > 0.:
                self.log += 'STATE DAMAGE: %s takes %s state damage from poison, hp reduces from %s to %s\n' % (
                    str(pkm), damage, before_hp, pkm.hp)

        return damage

    def _get_attack_order(self) -> Tuple[int, int]:
        """
        Get attack order for this turn.
        Priority is given to the pkm with highest speed_stage. Otherwise random.

        :return: tuple with first and second trainer to perform attack
        """
        if self.speed_stage[0] > self.speed_stage[1]:
            order = [0, 1]
        elif self.speed_stage[0] < self.speed_stage[1]:
            order = [1, 0]
        else:
            # random attack order
            order = [0, 1]
            np.random.shuffle(order)

        return order[0], order[1]

    def reset(self):
        self.weather = WeatherCondition.CLEAR
        self.attack_stage = [0, 0]
        self.defense_stage = [0, 0]
        self.speed_stage = [0, 0]
        self.spikes = [0, 0]
        self.confused = [0, 0]
        self.n_turns_no_clear = 0
        self.switched = [False, False]

        # random setting
        self.a_pkm = [Pkm(), Pkm()]
        self.p_pkm = [[Pkm() for _ in range(self.party_size)],
                      [Pkm() for _ in range(self.party_size)]]  # party pokemons

        if self.debug:
            self.log += 'TRAINER 0\nActive pokemon: %s\nParty pokemon: %s, %s, %s, %s, %s\n' % (
                str(self.a_pkm[0]), str(self.p_pkm[0][0]), str(self.p_pkm[0][1]), str(self.p_pkm[0][2]),
                str(self.p_pkm[0][3]), str(self.p_pkm[0][4]))
            self.log += 'TRAINER 1\nActive pokemon: %s\nParty pokemon: %s, %s, %s, %s, %s\n' % (
                str(self.a_pkm[1]), str(self.p_pkm[1][0]), str(self.p_pkm[1][1]), str(self.p_pkm[1][2]),
                str(self.p_pkm[1][3]), str(self.p_pkm[1][4]))

        return [self._state_trainer(0), self._state_trainer(1)]

    def render(self, mode='human'):
        print(self.log)

    def _state_trainer(self, t_id: int):
        """
        Get trainer view of the battle.

        :param t_id: trainer
        :return: observation state of the trainer
        """
        opponent = not t_id
        pkm = self.a_pkm[t_id]
        opponent_pkm = self.a_pkm[opponent]
        moves = pkm.moves
        party = self.p_pkm[t_id]
        return [
            # active pkm
            pkm.type, pkm.hp, pkm.status,
            # opponent active pkm
            opponent_pkm.type, opponent_pkm.hp, opponent_pkm.status,
            # party pkm
            party[0].type, party[0].hp, party[0].status,
            party[1].type, party[1].hp, party[1].status,
            party[2].type, party[2].hp, party[2].status,
            party[3].type, party[3].hp, party[3].status,
            party[4].type, party[4].hp, party[4].status,
            # active pkm moves
            moves[0].type, moves[0].power,
            moves[1].type, moves[1].power,
            moves[2].type, moves[2].power,
            moves[3].type, moves[3].power,
            # field effects
            self.attack_stage[t_id], self.attack_stage[opponent],
            self.defense_stage[t_id], self.defense_stage[opponent],
            self.speed_stage[t_id], self.speed_stage[opponent],
            self.spikes[t_id], self.spikes[opponent],
            pkm.n_turns_asleep, opponent_pkm.n_turns_asleep,
            self.confused[t_id], self.confused[opponent],
            self.weather
        ]

    def _switch_pkm(self, t_id: int, s_pos: int):
        """
        Switch active pkm of trainer id with party pkm on s_pos.
        Random party pkm if s_pos = -1

        :param t_id: trainer id
        :param s_pos: to be switch pokemon party position
        """
        # identify fainted pkm
        not_fainted_pkm = self._get_not_fainted_pkms(t_id)
        all_party_fainted = not not_fainted_pkm
        all_fainted = all_party_fainted and self.a_pkm[t_id].fainted()

        if not all_fainted:

            # select random party pkm to switch if needed
            if not all_party_fainted:
                if s_pos == -1:
                    np.random.shuffle(not_fainted_pkm)
                    s_pos = not_fainted_pkm[0]

                # switch party and bench pkm
                active = self.a_pkm[t_id]
                self.a_pkm[t_id] = self.p_pkm[t_id][s_pos]
                self.p_pkm[t_id][s_pos] = active

                if self.debug:
                    self.log += 'SWITCH: Trainer %s switches %s with %s in party\n' % (
                        t_id, str(active), str(self.a_pkm[t_id]))

                # clear switch states
                self.attack_stage[t_id] = 0
                self.defense_stage[t_id] = 0
                self.speed_stage[t_id] = 0
                self.confused[t_id] = 0

                self.switched[t_id] = True

    def _get_attack_dmg_rcvr(self, t_id: int, m_id: int) -> Tuple[float, float]:
        """
        Get damage and recover done by an attack m_id of active pkm of trainer t_id

        :param t_id: trainer of the active pkm
        :param m_id: move of the active pkm
        :return: damage, recover
        """

        move = self.a_pkm[t_id].moves[m_id]
        pkm = self.a_pkm[t_id]
        opponent = not t_id
        opponent_pkm = self.a_pkm[not t_id]
        damage = 0.
        recover = 0.

        if move.power == 0. and move.type != PkmType.DRAGON and move.type != PkmType.GHOST:
            # weather moves
            if move.type == PkmType.FIRE and self.weather != WeatherCondition.SUNNY:  # SUNNY DAY (FIRE)
                self.weather = WeatherCondition.SUNNY
                self.n_turns_no_clear = 0
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses sunny day\n' % (t_id, str(pkm))
            elif move.type == PkmType.WATER and self.weather != WeatherCondition.RAIN:  # RAIN DANCE (WATER)
                self.weather = WeatherCondition.RAIN
                self.n_turns_no_clear = 0
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses rain dance\n' % (t_id, str(pkm))
            elif move.type == PkmType.ICE and self.weather != WeatherCondition.HAIL:  # HAIL (ICE)
                self.weather = WeatherCondition.HAIL
                self.n_turns_no_clear = 0
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses hail\n' % (t_id, str(pkm))
            elif move.type == PkmType.ROCK and self.weather != WeatherCondition.SANDSTORM:  # SANDSTORM (ROCK)
                self.weather = WeatherCondition.SANDSTORM
                self.n_turns_no_clear = 0
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses sandstorm\n' % (t_id, str(pkm))

            # status moves
            elif move.type == PkmType.ELECTRIC:  # THUNDER WAVE (ELECTRIC)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses thunder wave\n' % (t_id, str(pkm))
                if opponent_pkm.type != PkmType.ELECTRIC and opponent_pkm.type != PkmType.GROUND:
                    if opponent_pkm.status != PkmStatus.PARALYZED:
                        opponent_pkm.status = PkmStatus.PARALYZED
                        if self.debug:
                            self.log += 'STATUS: %s was paralyzed\n' % (str(opponent_pkm))

            elif move.type == PkmType.POISON:  # POISON (POISON)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses poison\n' % (t_id, str(pkm))
                if opponent_pkm.type != PkmType.POISON and opponent_pkm.type != PkmType.STEEL:
                    if not opponent_pkm.status != PkmStatus.POISONED:
                        opponent_pkm.status = PkmStatus.POISONED
                        if self.debug:
                            self.log += 'STATUS: %s was poisoned\n' % (str(opponent_pkm))
            elif move.type == PkmType.GRASS:  # SPORE (GRASS)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses spore\n' % (t_id, str(pkm))
                if opponent_pkm.status != PkmStatus.SLEEP:
                    opponent_pkm.status = PkmStatus.SLEEP
                    if self.debug:
                        self.log += 'STATUS: %s fell asleep\n' % (str(opponent_pkm))

            # other moves
            elif move.type == PkmType.FAIRY:  # SWEET KISS (FAIRY)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses sweet kiss\n' % (t_id, str(pkm))
                if not self.confused[not t_id]:
                    self.confused[not t_id] = True
                    if self.debug:
                        self.log += 'STATUS: %s is confused\n' % t_id, str(opponent_pkm)
            elif move.type == PkmType.GROUND:  # SPIKES (GROUND)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses spikes\n' % (t_id, str(pkm))
                self.spikes[not t_id] += 1
            elif move.type == PkmType.DARK or move.type == PkmType.FIGHT:  # NASTY PLOT (DARK) or BULK UP (FIGHT)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses nasty plot/bulk up\n' % (t_id, str(pkm))
                if self.attack_stage[t_id] < 5:
                    self.attack_stage[t_id] += 1
                    if self.debug:
                        self.log += 'STAGE: %s attack increased\n' % (str(pkm))
            elif move.type == PkmType.PSYCHIC or move.type == PkmType.STEEL:  # CALM MIND (PSYCHIC) or IRON DEFENSE (STEEL)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses calm mind/iron defense\n' % (t_id, str(pkm))
                if self.defense_stage[t_id] < 5:
                    self.defense_stage[t_id] += 1
                    if self.debug:
                        self.log += 'STAGE: %s defense increased\n' % (str(pkm))
            elif move.type == PkmType.BUG:  # STRING SHOT (BUG)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses string shot\n' % (t_id, str(pkm))
                if self.speed_stage[t_id] > -5:
                    self.speed_stage[opponent] -= 1
                    if self.debug:
                        self.log += 'STAGE: %s speed decreases\n' % (str(opponent_pkm))
            elif move.type == PkmType.FLYING or move.type == PkmType.NORMAL:  # ROOST (FLYING) or RECOVER (NORMAL)
                recover = HIT_POINTS / 2.
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses roost/recover\n' % (t_id, str(pkm))

        else:
            # battle move
            if move.power == 0. and move.type == PkmType.DRAGON:  # DRAGON RAGE (DRAGON)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses dragon rage\n' % (t_id, str(pkm))
                if opponent_pkm.type != PkmType.FAIRY:
                    damage = 40.
            elif move.power == 0. and move.type == PkmType.GHOST:  # NIGHT SHADE (GHOST)
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses night shade\n' % (t_id, str(pkm))
                if opponent_pkm.type != PkmType.NORMAL:
                    damage = 40.
            else:
                if self.debug:
                    self.log += 'MOVE: Trainer %s with %s uses %s\n' % (t_id, str(pkm), str(move))
                stab = 1.5 if move.type == pkm.type else 1.
                if (move.type == PkmType.WATER and self.weather == WeatherCondition.RAIN) or (
                        move.type == PkmType.FIRE and self.weather == WeatherCondition.SUNNY):
                    weather = 1.5
                elif (move.type == PkmType.WATER and self.weather == WeatherCondition.SUNNY) or (
                        move.type == PkmType.FIRE and self.weather == WeatherCondition.RAIN):
                    weather = .5
                else:
                    weather = 1.
                stage_level = self.attack_stage[t_id] - self.defense_stage[opponent]
                stage = (stage_level + 2.) / 2 if stage_level >= 0. else 2. / (np.abs(stage_level) + 2.)
                damage = TYPE_CHART_MULTIPLIER[move.type][
                             opponent_pkm.type] * stab * weather * stage * move.power

        return damage, recover

    def _perform_pkm_attack(self, t_id: int, m_id: int) -> Tuple[float, float]:
        """
        Perform a pkm attack

        :param t_id: trainer
        :param m_id: move
        :return: reward, recover
        """
        damage, recover = 0., 0.

        if m_id < N_MOVES:
            opponent = not t_id
            pkm = self.a_pkm[t_id]
            before_hp = pkm.hp
            opp_pkm = self.a_pkm[opponent]
            before_opp_hp = opp_pkm.hp

            # get damage and recover values from attack
            damage_2_deal, health_2_recover = self._get_attack_dmg_rcvr(t_id, m_id)

            # perform recover
            pkm.hp += health_2_recover
            pkm.hp = HIT_POINTS if pkm.hp > HIT_POINTS else pkm.hp
            recover = pkm.hp - before_hp
            if self.debug and recover > 0.:
                self.log += 'RECOVER: recovers %s\n' % recover

            # perform damage
            opp_pkm.hp -= damage_2_deal
            opp_pkm.hp = 0. if opp_pkm.hp < 0. else opp_pkm.hp
            damage = before_opp_hp - opp_pkm.hp
            if self.debug and damage > 0.:
                self.log += 'DAMAGE: deals %s damage, hp reduces from %s to %s for %s\n' % (
                    damage, before_opp_hp, opp_pkm.hp, str(opp_pkm))

        return damage, recover

    def _get_not_fainted_pkms(self, t_id: int) -> List[int]:
        """
        Return a list of position of not fainted pkm in trainer t_id party.

        :param t_id: trainer
        """
        not_fainted_pkm = []
        for i, p in enumerate(self.p_pkm[t_id]):
            if not p.fainted():
                not_fainted_pkm.append(i)
        return not_fainted_pkm

    def _fainted_team(self, t_id: int) -> bool:
        """
        Check if trainer t_id team is fainted

        :param t_id: trainer team to check
        :return: True if entire team is fainted
        """
        for i in range(N_PARTY):
            if not self.p_pkm[t_id][i].fainted():
                return False
        return self.a_pkm[t_id].fainted()

    def __get_pre_combat_damage(self, t_id: int) -> float:
        """
        Check if trainer t_id active pkm is confused this turn and cannot move and take damage.

        :param t_id: trainer
        :return: 0. if not confused or damage to take if confused
        """
        return STATE_DAMAGE if self.confused[t_id] and random.uniform(0, 1) <= 0.33 else 0.

    def __switch_fainted_pkm(self) -> Tuple[float, float]:
        """

        :return:
        """
        damage0, damage1 = 0., 0.
        self.switched = [False, False]
        if self.a_pkm[0].fainted():
            if self.debug:
                self.log += 'FAINTED: %s\n' % (str(self.a_pkm[0]))
            self._switch_pkm(0, -1)
        if self.a_pkm[1].fainted():
            if self.debug:
                self.log += 'FAINTED: %s\n' % (str(self.a_pkm[1]))
            self._switch_pkm(1, -1)
        if not self.a_pkm[0].fainted():
            damage0 = self._get_entry_hazard_damage(0)
        if not self.a_pkm[1].fainted():
            damage1 = self._get_entry_hazard_damage(1)
        d0, d1 = 0., 0.
        if (self.a_pkm[0].fainted() or self.a_pkm[1].fainted()) and (
                not self._fainted_team(0) and not self._fainted_team(1)):
            d0, d1 = self.__switch_fainted_pkm()
        return damage0 + d0, damage1 + d1



