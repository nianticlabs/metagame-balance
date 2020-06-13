import gym
from gym import spaces
import random
import numpy as np

# TODO remake logs

# type codification
NORMAL = 0
FIRE = 1
WATER = 2
ELECTRIC = 3
GRASS = 4
ICE = 5
FIGHT = 6
POISON = 7
GROUND = 8
FLYING = 9
PSYCHIC = 10
BUG = 11
ROCK = 12
GHOST = 13
DRAGON = 14
DARK = 15
STEEL = 16
FAIRY = 17

TYPE_TO_STR = {NORMAL: "NORMAL", FIRE: "FIRE", WATER: "WATER", ELECTRIC: "ELECTRIC", GRASS: "GRASS", ICE: "ICE",
               FIGHT: "FIGHT", POISON: "POISON", GROUND: "GROUND", FLYING: "FLYING", PSYCHIC: "PSYCHIC", BUG: "BUG",
               ROCK: "ROCK", GHOST: "GHOST", DRAGON: "DRAGON", DARK: "DARK", STEEL: "STEEL", FAIRY: "FAIRY"}
TYPE_LIST = [NORMAL, FIRE, WATER, ELECTRIC, GRASS, ICE, FIGHT, POISON, GROUND, FLYING, PSYCHIC, BUG, ROCK, GHOST,
             DRAGON, DARK, STEEL, FAIRY]
N_TYPES = len(TYPE_LIST)

# type chart
TYPE_CHART_MULTIPLIER = [
    [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., .5, .0, 1., 1., .5, 1.],  # NORMAL
    [1., .5, .5, 1., 2., 2., 1., 1., 1., 1., 1., 2., .5, 1., .5, 1., 2., 1.],  # FIRE
    [1., 2., .5, 1., .5, 1., 1., 1., 2., 1., 1., 1., 2., 1., .5, 1., 1., 1.],  # WATER
    [1., 1., 2., .5, .5, 1., 1., 1., 0., 2., 1., 1., 1., 1., .5, 1., 1., 1.],  # ELECTRIC
    [1., .5, 2., 1., .5, 1., 1., .5, 2., .5, 1., .5, 2., 1., .5, 1., .5, 1.],  # GRASS
    [1., .5, .5, 1., 2., .5, 1., 1., 2., 2., 1., 1., 1., 1., 2., 1., .5, 1.],  # ICE
    [2., 1., 1., 1., 1., 2., 1., .5, 1., .5, .5, .5, 2., 0., 1., 2., 2., .5],  # FIGHTING
    [1., 1., 1., 1., 2., 1., 1., .5, .5, 1., 1., 1., .5, .5, 1., 1., .0, 2.],  # POISON
    [1., 2., 1., 2., .5, 1., 1., 2., 1., 0., 1., .5, 2., 1., 1., 1., 2., 1.],  # GROUND
    [1., 1., 1., .5, 2., 1., 2., 1., 1., 1., 1., 2., .5, 1., 1., 1., .5, 1.],  # FLYING
    [1., 1., 1., 1., 1., 1., 2., 2., 1., 1., .5, 1., 1., 1., 1., 0., .5, 1.],  # PSYCHIC
    [1., .5, 1., 1., 2., 1., .5, .5, 1., .5, 2., 1., 1., .5, 1., 2., .5, .5],  # BUG
    [1., 2., 1., 1., 1., 2., .5, 1., .5, 2., 1., 2., 1., 1., 1., 1., .5, 1.],  # ROCK
    [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 2., 1., 1., 2., 1., .5, 1., 1.],  # GHOST
    [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 2., 1., .5, .0],  # DRAGON
    [1., 1., 1., 1., 1., 1., .5, 1., 1., 1., 2., 1., 1., 2., 1., .5, 1., .5],  # DARK
    [1., .5, .5, .5, 1., 2., 1., 1., 1., 1., 1., 1., 2., 1., 1., 1., .5, 2.],  # STEEL
    [1., .5, 1., 1., 1., 1., 2., .5, 1., 1., 1., 1., 1., 1., 2., 2., .5, 1.]  # FAIRY
]

# trainers
N_TRAINERS = 2
N_PARTY = 5

# move power range
POWER_MIN = 50.
POWER_MAX = 100.

# number moves
N_MOVES = 4
N_SWITCHES = 5

# hit Points
HIT_POINTS = POWER_MAX + POWER_MIN + 150.
STATE_DAMAGE = HIT_POINTS / 8.

# settings
SETTING_RANDOM = 0
SETTING_FULL_DETERMINISTIC = 1
SETTING_HALF_DETERMINISTIC = 2
SETTING_FAIR_IN_ADVANTAGE = 3

# weather
CLEAR = 0
SUNNY = 1
RAIN = 2
SANDSTORM = 3
HAIL = 4

WEATHER_TO_STR = {CLEAR: "CLEAR", SUNNY: "SUNNY", RAIN: "RAIN", SANDSTORM: "SANDSTORM", HAIL: "HAIL"}

# status
NONE = 0
PARALYZED = 1
POISONED = 2
CONFUSED = 3
SLEEP = 4

STATUS_TO_STR = {NONE: "", PARALYZED: "PARALYZED", POISONED: "POISONED", CONFUSED: "CONFUSED", SLEEP: "SLEEP"}


class Move:
    def __init__(self, move_type=None, move_power=None, my_type=None):
        if move_type is None:
            if my_type is None:
                self.type = random.randrange(0, N_TYPES)
            else:
                self.type = random.randrange(0, N_TYPES)
                # Don't pick attacks that are super effective against self or that self is super effective against
                while (TYPE_CHART_MULTIPLIER[self.type][my_type] > 1 or
                       TYPE_CHART_MULTIPLIER[my_type][self.type] > 1):
                    self.type = random.randrange(0, N_TYPES)
        else:
            self.type = move_type
        if move_power is None:
            self.power = random.randrange(POWER_MIN, POWER_MAX) * 1.
        else:
            self.power = move_power

    def __str__(self):
        return "Move(" + TYPE_TO_STR[self.type] + ", " + str(self.power) + ")"


class Pkm:
    def __init__(self, p_type=None, hp=HIT_POINTS,
                 type0=None, type0power=None, type1=None, type1power=None,
                 type2=None, type2power=None, type3=None, type3power=None):
        self.hp = hp
        self.status = NONE
        self.n_turn_asleep = 0
        if p_type is None:
            self.p_type = random.randrange(0, N_TYPES)
            self.moves = [Move(my_type=self.p_type) for _ in range(N_MOVES - 1)] + [
                Move(move_type=self.p_type)]
        else:
            self.p_type = p_type
            self.moves = [Move(move_type=type0, move_power=type0power),
                          Move(move_type=type1, move_power=type1power),
                          Move(move_type=type2, move_power=type2power),
                          Move(move_type=type3, move_power=type3power)]

    def __str__(self):
        return 'Pokemon(' + TYPE_TO_STR[self.p_type] + ', HP ' + str(self.hp) + ', Status ' + STATUS_TO_STR[
            self.status] + ', ' + str(self.moves[0]) + ', ' + str(self.moves[1]) + ', ' + str(
            self.moves[2]) + ', ' + str(self.moves[3]) + ')'


class PkmBattleEnv(gym.Env):
    def __init__(self, setting=SETTING_RANDOM, debug=False):
        self.numberOfActions = N_MOVES + 1
        self.a_pkm = [Pkm(), Pkm()]  # active pokemons
        self.p_pkm = [[Pkm(), Pkm(), Pkm(), Pkm(), Pkm()], [Pkm(), Pkm(), Pkm(), Pkm(), Pkm()]]  # party pokemons
        self.setting = setting
        self.action_space = spaces.Discrete(N_MOVES + N_SWITCHES)
        self.observation_space = spaces.Discrete(len(encode(self._state_trainer(0))))
        self.weather = CLEAR
        self.attack_stage = [0., 0.]
        self.defense_stage = [0., 0.]
        self.speed_stage = [0, 0]
        self.spikes = [0, 0]
        self.seeds = [0, 0]
        self.confused = [0, 0]
        self.n_turns_no_clear = 0
        self.n_turns_confused = [0, 0]
        self.switched = [False, False]

    def step(self, actions):  # TODO finish battle logic

        # Reset variables
        r = [0., 0.]
        t = [False, False]

        # switch pkm
        self._process_switch_pkms(actions)

        # set trainer attack order
        first, second = self._get_attack_order()
        first_pkm = self.a_pkm[first]
        second_pkm = self.a_pkm[first]

        # get entry hazard damage
        dmg_2_first = self._get_entry_hazard_damage(first)
        dmg_2_second = self._get_entry_hazard_damage(second)

        r[first] = (dmg_2_second - dmg_2_first) / HIT_POINTS
        r[second] = (dmg_2_first - dmg_2_second) / HIT_POINTS

        first_can_attack = fainted_pkm(first_pkm)
        second_can_attack = fainted_pkm(second_pkm)

        # process all pre battle effects
        self._process_pre_battle_effects()

        # confusion state damage
        dmg_2_first = self._get_pre_combat_damage(first) if first_can_attack else 0.
        dmg_2_second = self._get_pre_combat_damage(second) if second_can_attack else 0.

        r[first] += (dmg_2_second - dmg_2_first) / HIT_POINTS
        r[second] += (dmg_2_first - dmg_2_second) / HIT_POINTS

        # battle
        first_can_attack = fainted_pkm(first_pkm) and self._check_paralyzed(first) and self._check_asleep(first)
        dmg_2_second, hp_2_first = self._perform_pkm_attack(first, actions[first]) if first_can_attack else 0., 0.

        second_can_attack = fainted_pkm(second_pkm) and self._check_paralyzed(second) and self._check_asleep(second)
        dmg_2_first, hp_2_second = self._perform_pkm_attack(first, actions[first]) if second_can_attack else 0., 0.

        r[first] += (dmg_2_second + hp_2_first - dmg_2_first) / HIT_POINTS + fainted_pkm(second_pkm)
        r[second] += (dmg_2_first + hp_2_second - dmg_2_second) / HIT_POINTS + fainted_pkm(first_pkm)

        # get post battle effects damage
        dmg_2_first = self._get_post_battle_damage(first) if first_can_attack else 0.
        dmg_2_second = self._get_post_battle_damage(second) if second_can_attack else 0.

        r[first] = (dmg_2_second - dmg_2_first) / HIT_POINTS
        r[second] = (dmg_2_first - dmg_2_second) / HIT_POINTS

        # process all post battle effects
        self._process_post_battle_effects()

        # switch fainted pkm


        # check if battle ended
        t[first] = self._fainted_team(first)
        t[second] = self._fainted_team(second)

        r[first] += t[first]
        r[second] += t[second]

        return [encode(self._state_trainer(0)), encode(self._state_trainer(1))], r, t[first] or t[second], None

    def _process_switch_pkms(self, actions):
        """
        Switch pokemons if players choosen to do so

        :param actions: players actions
        :return:
        """
        if actions[0] >= N_MOVES:
            switch_action = actions[0] - N_MOVES
            if not fainted_pkm(self.p_pkm[0][switch_action]):
                self._switch_pkm(0, switch_action)
        if actions[1] == N_MOVES:
            switch_action = actions[1] - N_MOVES
            if not fainted_pkm(self.p_pkm[1][switch_action]):
                self._switch_pkm(1, switch_action)

    def _get_entry_hazard_damage(self, t_id):
        """
        Get triggered damage to be dealt to a switched pkm.

        :param: t_id: owner trainer
        :return: damage to first pkm, damage to second pkm
        """
        damage = 0.

        # Spikes damage
        if self.spikes[t_id] and self.a_pkm[t_id].p_type != FLYING and self.switched[t_id]:
            pkm = self.a_pkm[t_id]
            before_hp = pkm.hp
            pkm.hp -= STATE_DAMAGE
            pkm.hp = 0. if pkm.hp < 0. else pkm.hp
            damage = before_hp - pkm.hp

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

            # check if active pkm should be no more asleep
            if self._check_asleep(pkm):
                pkm.n_turns_asleep += 1
                if random.uniform(0, 1) <= 0.5 or pkm.n_turns_asleep == 4:
                    pkm.status = NONE
                    pkm.n_turns_asleep = 0

    def _process_post_battle_effects(self):
        """
        Process all post battle effects.

        """
        if self.weather != CLEAR:
            self.n_turns_no_clear += 1

            # clear weather if appropriated
            if self.n_turns_no_clear > 5:
                self.weather = CLEAR
                self.n_turns_no_clear = 0

    def _get_post_battle_damage(self, t_id):
        """
        Get triggered damage to be dealt to switched pkm.

        :param: t_id: owner trainer
        :return: damage to pkm
        """
        pkm = self.a_pkm[t_id]
        damage = 0.

        if self.weather == SANDSTORM and (pkm.p_type != ROCK and pkm.p_type != GROUND and pkm.p_type != STEEL):
            damage += STATE_DAMAGE
        elif self.weather == HAIL and (pkm.p_type != ICE):
            damage += STATE_DAMAGE

        if damage >= pkm.hp:
            return damage

        if pkm.status == POISONED:
            damage += STATE_DAMAGE
        return damage

    def _get_attack_order(self):
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
        self.weather = CLEAR
        self.attack_stage = [0., 0.]
        self.defense_stage = [0., 0.]
        self.speed_stage = [0, 0]
        self.spikes = [0, 0]
        self.seeds = [0, 0]
        self.confused = [0, 0]
        self.n_turns_no_clear = 0
        self.switched = [False, False]

        # Random Setting
        if self.setting == SETTING_RANDOM:
            self.a_pkm = [Pkm(), Pkm()]  # active pokemons
            self.p_pkm = [[Pkm(), Pkm(), Pkm(), Pkm(), Pkm()], [Pkm(), Pkm(), Pkm(), Pkm(), Pkm()]]  # party pokemons
        elif self.setting == SETTING_FULL_DETERMINISTIC:  # TODO
            self.a_pkm = [Pkm(GRASS, HIT_POINTS, GRASS, 90, FIRE, 90, GRASS, 90, FIRE, 90),
                          Pkm(FIRE, HIT_POINTS, FIRE, 90, FIRE, 90, FIRE, 90, FIRE, 90)]  # active pokemons
            self.p_pkm = [Pkm(WATER, HIT_POINTS, FIGHT, 90, NORMAL, 90, NORMAL, 90, WATER, 90),
                          Pkm(NORMAL, HIT_POINTS, NORMAL, 90, NORMAL, 90, NORMAL, 90, NORMAL,
                              90)]  # party pokemons

        # Half Deterministic Setting
        elif self.setting == SETTING_HALF_DETERMINISTIC:
            if random.uniform(0, 1) <= 0.2:
                type1 = random.randrange(0, N_TYPES - 1)
                type2 = get_super_effective_move(type1)
                self.a_pkm = [Pkm(type1, HIT_POINTS, type1, 90, type2, 90, type1, 90, type2, 90),
                              Pkm(type2, HIT_POINTS, type2, 90, type2, 90, type2, 90, type2,
                                  90)]  # active pokemons
            else:
                self.a_pkm = [Pkm(), Pkm()]  # active pokemons
            self.p_pkm = [[Pkm(), Pkm(), Pkm(), Pkm(), Pkm()], [Pkm(), Pkm(), Pkm(), Pkm(), Pkm()]]  # party pokemons

        # Fair in Advantage Setting
        elif self.setting == SETTING_FAIR_IN_ADVANTAGE:
            type1 = random.randrange(0, N_TYPES - 1)
            type2 = get_super_effective_move(type1)
            self.a_pkm = [
                Pkm(type1, get_non_very_effective_move(type2), 90, get_non_very_effective_move(type2), 90,
                    get_effective_move(type2), 90, type1, 90),
                Pkm(type2, get_super_effective_move(type1), 90, get_non_very_effective_move(type1), 90,
                    get_effective_move(type1), 90, type2, 90)]  # active pokemons
            self.p_pkm = [[Pkm(), Pkm(), Pkm(), Pkm(), Pkm()], [Pkm(), Pkm(), Pkm(), Pkm(), Pkm()]]  # party pokemons

        return [encode(self._state_trainer(0)), encode(self._state_trainer(1))]

    def render(self, mode='human'):
        """
        if self.debug:
            if self.debug_message[0] != '' and self.debug_message[1] != '':
                if self.switched[0]:
                    if self.has_fainted:
                        print('Trainer 1', self.debug_message[1])
                        print('Trainer 0', self.debug_message[0])
                    else:
                        print('Trainer 0', self.debug_message[0])
                        print('Trainer 1', self.debug_message[1])
                elif self.switched[1]:
                    if self.has_fainted:
                        print('Trainer 0', self.debug_message[0])
                        print('Trainer 1', self.debug_message[1])
                    else:
                        print('Trainer 1', self.debug_message[1])
                        print('Trainer 0', self.debug_message[0])
                elif self.first == 0:
                    print('Trainer 0', self.debug_message[0])
                    print('Trainer 1', self.debug_message[1])
                else:
                    print('Trainer 1', self.debug_message[1])
                    print('Trainer 0', self.debug_message[0])
            print()
        print('Trainer 0')
        print('Active', self.a_pkm[0])
        print('Party', self.p_pkm[0])
        print('Trainer 1')
        print('Active', self.a_pkm[1])
        if mode != 'player':
            print('Party', self.p_pkm[1])
        print()
        """
        pass

    def change_setting(self, setting):
        self.setting = setting

    def _state_trainer(self, t_id):  # TODO
        opponent = not t_id
        return [
            # active pkm
            self.a_pkm[t_id].p_type, self.a_pkm[t_id].hp,
            # active pkm moves
            self.a_pkm[t_id].moves[0].type, self.a_pkm[t_id].moves[0].power,
            self.a_pkm[t_id].moves[1].type, self.a_pkm[t_id].moves[1].power,
            self.a_pkm[t_id].moves[2].type, self.a_pkm[t_id].moves[2].power,
            self.a_pkm[t_id].moves[3].type, self.a_pkm[t_id].moves[3].power,
            # party pkm moves
            self.p_pkm[t_id][0].p_type, self.p_pkm[t_id][0].hp,
            self.p_pkm[t_id][1].p_type, self.p_pkm[t_id][1].hp,
            self.p_pkm[t_id][2].p_type, self.p_pkm[t_id][2].hp,
            self.p_pkm[t_id][3].p_type, self.p_pkm[t_id][3].hp,
            self.p_pkm[t_id][4].p_type, self.p_pkm[t_id][4].hp,
            # opponent active pkm
            self.a_pkm[opponent].p_type, self.a_pkm[opponent].hp,
            # opponent party pkm
            self.p_pkm[opponent][0].p_type, self.p_pkm[opponent][0].hp,
            self.p_pkm[opponent][1].p_type, self.p_pkm[opponent][1].hp,
            self.p_pkm[opponent][2].p_type, self.p_pkm[opponent][2].hp,
            self.p_pkm[opponent][3].p_type, self.p_pkm[opponent][3].hp,
            self.p_pkm[opponent][4].p_type, self.p_pkm[opponent][4].hp]

    def _switch_pkm(self, t_id, s_pos):
        """
        Switch active pkm of trainer id with party pkm on s_pos.
        Random party pkm if s_pos = -1

        :param t_id: trainer id
        :param s_pos: to be switch pokemon party position
        """
        # identify fainted pkm
        not_fainted_pkm = self._get_not_fainted_pkms(t_id)
        all_fainted = not not_fainted_pkm

        if not all_fainted:

            # select random party pkm to switch if needed
            if s_pos == -1 or self.p_pkm[t_id][s_pos].hp != 0:
                np.random.shuffle(not_fainted_pkm)
                s_pos = not_fainted_pkm[0]

            # switch party and bench pkm
            temp = self.a_pkm[t_id]
            self.a_pkm[t_id] = self.p_pkm[t_id][s_pos]
            self.p_pkm[t_id][s_pos] = temp

            # clear switch states
            self.attack_stage[t_id] = 0
            self.defense_stage[t_id] = 0
            self.speed_stage[t_id] = 0
            self.seeds[t_id] = 0
            self.confused[t_id] = 0

            self.switched[t_id] = True

    def _get_attack_dmg_rcvr(self, t_id, m_id):
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

        if move.power == 0. and move.type != DRAGON and move.type != GHOST:
            # weather moves
            if move.type == FIRE:  # SUNNY DAY (FIRE)
                self.weather = SUNNY
            elif move.type == WATER:  # RAIN DANCE (WATER)
                self.weather = RAIN
            elif move.type == ICE:  # HAIL (ICE)
                self.weather = HAIL
            elif move.type == ROCK:  # SANDSTORM (ROCK)
                self.weather = SANDSTORM

            # status moves
            elif move.type == ELECTRIC:  # THUNDER WAVE (ELECTRIC)
                if opponent_pkm.p_type != ELECTRIC and opponent_pkm.p_type != GROUND:
                    opponent_pkm.status = PARALYZED
            elif move.type == POISON:  # POISON (POISON)
                if opponent_pkm.p_type != POISON and opponent_pkm.p_type != STEEL:
                    opponent_pkm.status = POISONED
            elif move.type == GRASS:  # SPORE (GRASS)
                opponent_pkm.status = SLEEP

            # other moves
            elif move.type == FAIRY:  # SWEET KISS (FAIRY)
                self.confused[not t_id] = True
            elif move.type == GROUND:  # SPIKES (GROUND)
                self.spikes[not t_id] = True
            elif move.type == DARK or move.type == FIGHT:  # NASTY PLOT (DARK) or BULK UP (FIGHT)
                self.attack_stage[t_id] += 1
            elif move.type == PSYCHIC or move.type == STEEL:  # CALM MIND (PSYCHIC) or IRON DEFENSE (STEEL)
                self.defense_stage[t_id] += 1
            elif move.type == BUG:  # STRING SHOT (BUG)
                self.speed_stage[not t_id] -= 1
            elif move.type == FLYING or move.type == NORMAL:  # ROOST (FLYING) or RECOVER (NORMAL)
                recover = HIT_POINTS / 2.

        else:
            # battle move
            if move.power == 0. and move.type == DRAGON:  # DRAGON RAGE (DRAGON)
                if opponent_pkm.p_type != FAIRY:
                    damage = 40.
            elif move.power == 0. and move.type == GHOST:  # NIGHT SHADE (GHOST)
                if opponent_pkm.p_type != NORMAL:
                    damage = 40.
            else:
                stab = 1.5 if move.type == pkm.p_type else 1.
                if (move.type == WATER and self.weather == RAIN) or (move.type == FIRE and self.weather == SUNNY):
                    weather = 1.5
                elif (move.type == WATER and self.weather == SUNNY) or (move.type == FIRE and self.weather == RAIN):
                    weather = .5
                else:
                    weather = 1.
                stage_level = self.attack_stage[t_id] - self.defense_stage[opponent]
                stage = (stage_level + 2.) / 2 if stage_level >= 0. else 2. / (stage_level + 2.)
                damage = TYPE_CHART_MULTIPLIER[move.type][opponent_pkm.p_type] * stab * weather * stage * move.power

        return damage, recover

    def _perform_pkm_attack(self, t_id, m_id):
        """
        Perform a pkm attack

        :param t_id: trainer id
        :param m_id: attack
        :return: reward, terminal, and whether target survived and can attack
        """
        damage, recover = 0., 0.

        if m_id < N_MOVES:
            opponent = not t_id

            pkm = self.a_pkm[t_id]
            opp_pkm = self.a_pkm[opponent]
            before_hp = pkm.hp
            before_opp_hp = opp_pkm.hp

            # get damage and recover values from attack
            damage_2_deal, health_2_recover = self._get_attack_dmg_rcvr(t_id, m_id)

            # perform recover
            pkm.hp += health_2_recover
            pkm.hp = HIT_POINTS if pkm.hp > HIT_POINTS else pkm.hp
            recover = before_hp - pkm.hp

            # perform damage
            opp_pkm.hp -= damage_2_deal
            opp_pkm.hp = 0. if opp_pkm.hp < 0. else opp_pkm.hp
            damage = before_opp_hp - opp_pkm.hp

        return damage, recover

    def _get_not_fainted_pkms(self, t_id):
        """
        Return a list of position of not fainted pkm in trainer t_id party.

        :param t_id: trainer
        """
        not_fainted_pkm = []
        for i, p in enumerate(self.p_pkm[t_id]):
            if fainted_pkm(p):
                not_fainted_pkm.append(i)
        return not_fainted_pkm

    def _check_paralyzed(self, t_id):
        """
        Check if trainer t_id active pkm is paralyzed this turn and cannot move.

        :param t_id: trainer
        :return: true if pkm is paralyzed and cannot move
        """
        if self.a_pkm[t_id].status == PARALYZED:
            return np.random.uniform(0, 1) <= 0.25
        else:
            return False

    def _check_confused(self, t_id):
        """
        Check if trainer t_id active pkm is confused this turn and cannot move and take damage.

        :param t_id: trainer
        :return: 0. if not confused or damage to take if confused
        """
        if self.confused[t_id] and random.uniform(0, 1) <= 0.33:
            return 40.
        else:
            return 0.

    def _check_asleep(self, t_id):
        """
        Check if trainer t_id active pkm is asleep this turn and cannot move.

        :param t_id: trainer
        :return: true if pkm is asleep and cannot move
        """
        return self.a_pkm[t_id].status == SLEEP

    def _fainted_team(self, t_id):
        """
        Check if trainer t_id team is fainted

        :param t_id: trainer team to check
        :return: True if entire team is fainted
        """
        for i in range(N_PARTY):
            if not fainted_pkm(self.p_pkm[t_id][i]):
                return False
        return True

    def _get_pre_combat_damage(self, first):
        pass


def fainted_pkm(pkm):
    """
    Check if pkm is fainted (hp == 0)

    :param pkm: pkm to check
    :return: True if pkm is fainted
    """
    return pkm.hp == 0


def encode(s):  # TODO
    """
    Encode Game state.

    :param s: game state
    :return: encoded game state in one hot vector
    """
    e = []
    for i in range(0, len(s) - 1):
        if i % 2 == 0:
            b = [0] * N_TYPES
            b[s[i]] = 1
            e += b
        else:
            e += [(s[i] / HIT_POINTS)]
    e += [(s[-1] / HIT_POINTS)]
    return e


def decode(e):  # TODO
    """
    Decode game state.

    :param e: encoded game state in one hot vector
    :return: game state
    """
    s = []
    index_e = 0
    for i in range(0, 7):
        for j in range(index_e, index_e + N_TYPES):
            if e[j] == 1:
                s.append(j % (N_TYPES + 1))
        index_e += N_TYPES
        s.append(e[index_e] * HIT_POINTS)
        index_e += 1
    s.append(e[index_e] * HIT_POINTS)
    return s


def get_super_effective_move(t):
    """
    Get a super effective move relative to type t.

    :param t: pokemon type
    :return: a random type that is super effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 2]
    if not s:
        print('Warning: Empty List!')
        return random.randrange(N_TYPES)
    return random.choice(s)


def get_non_very_effective_move(t):
    """
    Get a non very effective move relative to type t.

    :param t: pokemon type
    :return: a random type that is not very effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 1 / 2]
    if not s:
        print('Warning: Empty List!')
        return random.randrange(N_TYPES)
    return random.choice(s)


def get_effective_move(t):
    """
    Get a effective move relative to type t.

    :param t: pokemon type
    :return: a random type that is not very effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 1]
    if not s:
        print('Warning: Empty List!')
        return random.randrange(N_TYPES)
    return random.choice(s)
