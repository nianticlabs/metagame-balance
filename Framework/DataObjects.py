from math import isclose
from typing import List, Tuple, Set
from Framework.DataConstants import MOVE_MED_PP, MAX_HIT_POINTS
from Framework.DataTypes import PkmType, PkmStatus, N_STATS, N_ENTRY_HAZARD, PkmStat, WeatherCondition, \
    PkmEntryHazard
import random
import numpy as np


class PkmMove:

    def __init__(self, power: float = 90., acc: float = 1., max_pp: int = MOVE_MED_PP,
                 move_type: PkmType = PkmType.NORMAL, name: str = None, priority: bool = False,
                 prob=0.0, target=1, recover=0.0, status: PkmStatus = PkmStatus.NONE,
                 stat: PkmStat = PkmStat.ATTACK, stage: int = 0, fixed_damage: float = 0.0,
                 weather: WeatherCondition = WeatherCondition.CLEAR, hazard: PkmEntryHazard = PkmEntryHazard.NONE):
        """
        Pokemon move data structure.

        :param power: move power
        :param acc: move accuracy
        :param max_pp: move max power points
        :param move_type: move type
        :param name: move name
        :param priority: move priority
        :param prob: move effect probability (only moves with probability greater than zero perform effects)
        :param target: move effect target, zero for self and 1 for opponent
        :param recover: move recover quantity, how much hit points to recover
        :param status: status the move effect changes
        :param stage: stage the move effect adds/subtracts from the status
        :param fixed_damage: effect fixed_damage to apply, not affected by resistance or weakness (if greater than zero)
        :param weather: effect activates a weather condition
        :param hazard: effect deploys and hazard enter condition on the opponent field
        """
        self.power = power
        self.acc = acc
        self.max_pp = max_pp
        self.pp = max_pp
        self.type = move_type
        self.name = name
        self.priority = priority
        self.prob = prob
        self.target = target
        self.recover = recover
        self.status = status
        self.stat = stat
        self.stage = stage
        self.fixed_damage = fixed_damage
        self.weather = weather
        self.hazard = hazard

    def __eq__(self, other):
        if self.power != other.power:
            return False
        if self.acc != other.acc:
            return False
        if self.max_pp != other.max_pp:
            return False
        if self.type != other.type:
            return False
        if self.priority != other.priority:
            return False
        if self.prob > 0.:
            if self.prob != other.prob:
                return False
            if self.target != self.target:
                return False
            if self.recover != self.recover:
                return False
            if self.status != self.status:
                return False
            if self.stat != self.stat:
                return False
            if self.stage != self.stage:
                return False
            if self.fixed_damage != self.fixed_damage:
                return False
            if self.weather != self.weather:
                return False
            if self.hazard != self.hazard:
                return False
        return True

    def __hash__(self):
        if self.prob == 0.:
            return hash((self.power, self.acc, self.max_pp, self.type, self.priority))
        return hash((self.power, self.acc, self.max_pp, self.type, self.priority, self.prob, self.target, self.recover,
                     self.status, self.stat, self.stage, self.fixed_damage, self.weather, self.hazard))

    def __str__(self):
        if self.name:
            return self.name
        name = "PkmMove(Power=%f, Acc=%f, PP=%d, Type=%s" % (self.power, self.acc, self.pp, self.type.name)
        if self.priority > 0:
            name += ", Priority=%d" % self.priority
        if self.prob > 0.:
            if self.prob < 1.:
                name += ", Prob=%f" % self.prob
            name += ", Target=Self" if self.target == 0 else ", Target=Opp"
            if self.recover > 0.:
                name += ", Recover=%f" % self.recover
            if self.status != PkmStatus.NONE:
                name += ", Status=%s" % self.status.name
            if self.stage != 0.:
                name += ", Stat=%s, Stage=%d" % (self.stat.name, self.stage)
            if self.fixed_damage > 0.:
                name += ", Fixed=%f" % self.fixed_damage
            if self.weather != self.weather.CLEAR:
                name += ", Weather=%s" % self.weather.name
            if self.hazard != PkmEntryHazard.NONE:
                name += ", Hazard=%s" % self.hazard.name
        return name + ")"

    def reset(self):
        self.pp = self.max_pp

    def effect(self, v):
        if random.random() < self.prob:
            v.set_recover(self.recover)
            v.set_fixed_damage(self.fixed_damage)
            if self.stage > 0:
                v.set_stage(self.stat, self.target, self.stage)
            if self.status != self.status.NONE:
                v.set_status(self.status, self.target)
            if self.weather != self.weather.CLEAR:
                v.set_weather(self.weather)
            if self.hazard != PkmEntryHazard.NONE:
                v.set_entry_hazard(self.hazard, self.target)


def get_move_view(move: PkmMove):
    class MoveView:

        def get_power(self) -> float:
            return move.power

        def get_acc(self) -> float:
            return move.acc

        def get_pp(self) -> int:
            return move.pp

        def get_type(self) -> PkmType:
            return move.type

        def get_priority(self) -> int:
            return move.priority

        def get_prob(self) -> float:
            return move.prob

        def get_target(self) -> int:
            return move.target

        def get_recover(self) -> float:
            return move.recover

        def get_status(self) -> PkmStatus:
            return move.status

        def get_stat(self) -> PkmStat:
            return move.stat

        def get_stage(self) -> int:
            return move.stage

        def get_fixed_damage(self) -> float:
            return move.fixed_damage

        def get_weather(self) -> WeatherCondition:
            return move.weather

        def get_hazard(self) -> PkmEntryHazard:
            return move.hazard

    return MoveView()


PkmMoveRoster = Set[PkmMove]


class Pkm:

    def __init__(self, p_type: PkmType = PkmType.NORMAL, max_hp: float = MAX_HIT_POINTS,
                 status: PkmStatus = PkmStatus.NONE, move0: PkmMove = PkmMove(), move1: PkmMove = PkmMove(),
                 move2: PkmMove = PkmMove(), move3: PkmMove = PkmMove()):
        """
        In battle Pokemon base data struct.

        :param p_type: pokemon type
        :param max_hp: max hit points
        :param status: current status (PARALYZED, ASLEEP, etc.)
        :param move0: first move
        :param move1: second move
        :param move2: third move
        :param move3: fourth move
        """
        self.type: PkmType = p_type
        self.max_hp: float = max_hp
        self.hp: float = max_hp
        self.status: PkmStatus = status
        self.n_turns_asleep: int = 0
        self.moves: List[PkmMove] = [move0, move1, move2, move3]

    def __eq__(self, other):
        return self.type == other.type and isclose(self.max_hp, other.max_hp) and set(self.moves) == set(other.moves)

    def __hash__(self):
        return hash((self.type, self.max_hp) + tuple(self.moves))

    def __str__(self):
        s = 'Pkm(Type=%s, HP=%d' % (self.type.name, self.hp)
        if self.status != PkmStatus.NONE:
            s += ', Status=%s' % self.status.name
            if self.status == PkmStatus.SLEEP:
                s += ', Turns Asleep=%d' % self.n_turns_asleep
        s += ', Moves={'
        for move in self.moves:
            s += str(move) + ', '
        return s + '})'

    def reset(self):
        """
        Reset Pkm stats.
        """
        self.hp = self.max_hp
        self.status = PkmStatus.NONE
        self.n_turns_asleep = 0
        for move in self.moves:
            move.reset()

    def fainted(self) -> bool:
        """
        Check if pkm is fainted (hp == 0).

        :return: True if pkm is fainted
        """
        return self.hp == 0

    def paralyzed(self) -> bool:
        """
        Check if pkm is paralyzed this turn and cannot move.

        :return: true if pkm is paralyzed and cannot move
        """
        return self.status == PkmStatus.PARALYZED and np.random.uniform(0, 1) <= 0.25

    def asleep(self) -> bool:
        """
        Check if pkm is asleep this turn and cannot move.

        :return: true if pkm is asleep and cannot move
        """
        return self.status == PkmStatus.SLEEP

    def frozen(self) -> bool:
        """
        Check if pkm is frozen this turn and cannot move.

        :return: true if pkm is frozen and cannot move
        """
        return self.status == PkmStatus.FROZEN


class PkmTemplate:

    def __init__(self, move_roster: PkmMoveRoster, pkm_type: PkmType, max_hp: float):
        """
        Pokemon specimen definition data structure.

        :param move_roster: set of available moves for Pokemon of this species
        :param pkm_type: pokemon type
        :param max_hp: pokemon max_hp
        """
        self.move_roster: PkmMoveRoster = move_roster
        self.type: PkmType = pkm_type
        self.max_hp = max_hp

    def __eq__(self, other):
        return self.type == other.type and self.max_hp == other.max_hp and self.move_roster == other.move_roster

    def __hash__(self):
        return hash((self.type, self.max_hp) + tuple(self.move_roster))

    def __str__(self):
        s = 'PkmTemplate(Type=%s, Max_HP=%d, Moves={' % (PkmType(self.type).name, self.max_hp)
        for move in self.move_roster:
            s += str(move) + ', '
        return s + '})'

    def gen_pkm(self, moves: List[int]) -> Pkm:
        """
        Given the indexes of the moves generate a pokemon of this species.

        :param moves: index list of moves
        :return: the requested pokemon
        """
        move_list = list(self.move_roster)
        return Pkm(p_type=self.type, max_hp=self.max_hp,
                   move0=move_list[moves[0]],
                   move1=move_list[moves[1]],
                   move2=move_list[moves[2]],
                   move3=move_list[moves[3]])

    def is_speciman(self, pkm: Pkm) -> bool:
        """
        Check if input pokemon is a speciman of this species

        :param pkm: pokemon
        :return: if pokemon is speciman of this template
        """
        return pkm.type == self.type and pkm.max_hp == self.max_hp and set(pkm.moves).issubset(self.move_roster)


def get_pkm_view(pkm: Pkm):
    class PkmView:

        def get_type(self) -> PkmType:
            return pkm.type

        def get_hp(self) -> float:
            return pkm.hp

        def get_pkm_status(self) -> PkmStatus:
            return pkm.status

        def get_n_turns_asleep(self) -> int:
            return pkm.n_turns_asleep

        def get_move_view(self, idx: int) -> get_move_view.MoveView:
            return pkm.moves[idx]

    return PkmView()


PkmRoster = Set[PkmTemplate]


class PkmTeam:

    def __init__(self, pkms: List[Pkm] = None):
        """
        In battle Pkm team.

        :param pkms: Chosen pokemon. The first stays the active pokemon.
        """
        if pkms is None:
            pkms = [Pkm()]
        self.active: Pkm = pkms.pop(0)
        self.party: List[Pkm] = pkms
        self.stage: List[int] = [0] * N_STATS
        self.confused: bool = False
        self.n_turns_confused: int = 0
        self.entry_hazard: List[int] = [0] * N_ENTRY_HAZARD

    def __eq__(self, other):
        eq = self.active == other.active and self.stage == other.stage and self.confused == other.confused and \
               self.n_turns_confused == other.n_turns_confused
        if not eq:
            return False
        for i, p in enumerate(self.party):
            if p != other.party[i]:
                return False
        for i, h in enumerate(self.entry_hazard):
            if h != other.entry_hazard[i]:
                return False
        return True

    def __str__(self):
        party = ''
        for i in range(0, len(self.party)):
            party += str(self.party[i]) + '\n'
        return 'Active:\n%s\nParty:\n%s' % (str(self.active), party)

    def reset(self):
        """
        Reset all pkm status from team and active pkm conditions.
        """
        self.active.reset()
        for pkm in self.party:
            pkm.reset()
        for i in range(len(self.stage)):
            self.stage[i] = 0
        self.confused = False
        self.n_turns_confused = 0
        for i in range(len(self.entry_hazard)):
            self.entry_hazard[i] = 0

    def reset_team_members(self, pkms: List[Pkm] = None):
        """
        Reset tean members

        :param pkms: list of pkm members
        """
        if pkms is None:
            pkms = [Pkm()]
        self.active: Pkm = pkms.pop(0)
        self.party: List[Pkm] = pkms
        self.reset()

    def size(self) -> int:
        """
        Get team size.

        :return: Team size. Number of party pkm plus 1
        """
        return len(self.party) + 1

    def fainted(self) -> bool:
        """
        Check if team is fainted

        :return: True if entire team is fainted
        """
        for i in range(len(self.party)):
            if not self.party[i].fainted():
                return False
        return self.active.fainted()

    def get_not_fainted(self) -> List[int]:
        """
        Check which pokemon are not fainted in party.

        :return: a list of positions of not fainted pkm in party.
        """
        not_fainted = []
        for i, p in enumerate(self.party):
            if not p.fainted():
                not_fainted.append(i)
        return not_fainted

    def switch(self, pos: int) -> Tuple[Pkm, Pkm]:
        """
        Switch active pkm with party pkm on pos.
        Random party pkm if s_pos = -1

        :param pos: to be switch pokemon party position
        :returns: new active pkm, old active pkm
        """
        if len(self.party) == 0:
            return self.active, self.active

        # identify fainted pkm
        not_fainted_pkm = self.get_not_fainted()
        all_party_fainted = not not_fainted_pkm
        all_fainted = all_party_fainted and self.active.fainted()

        if not all_fainted:

            # select random party pkm to switch if needed
            if not all_party_fainted:
                if pos == -1:
                    np.random.shuffle(not_fainted_pkm)
                    pos = not_fainted_pkm[0]

                # switch party and bench pkm
                active = self.active
                self.active = self.party[pos]
                self.party[pos] = active

                # clear
                self.stage = [0] * N_STATS
                self.confused = False

        return self.active, self.party[pos]


def get_team_view(team: PkmTeam):
    class PkmTeamView:

        def get_active_pkm_view(self) -> get_pkm_view.PkmView:
            return get_pkm_view(team.active)

        def get_party_pkm_view(self, idx: int) -> get_pkm_view.PkmView:
            return get_pkm_view(team.party[idx])

        def get_stage(self, stat: PkmStat) -> int:
            return team.stage[stat]

        def get_confused(self) -> bool:
            return team.confused

        def get_n_turns_confused(self) -> int:
            return team.n_turns_confused

        def get_entry_hazard(self, hazard: PkmEntryHazard) -> int:
            return team.entry_hazard[hazard]

    return PkmTeamView()


class MetaData:
    pass
