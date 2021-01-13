from typing import List, Tuple, Set
from Framework.DataConstants import MOVE_MED_PP, TYPE_CHART_MULTIPLIER, MAX_HIT_POINTS
from Framework.DataTypes import PkmType, N_TYPES, PkmStatus, N_STATS, N_ENTRY_HAZARD, PkmStat, WeatherCondition, \
    PkmEntryHazard
import random
import numpy as np


class PkmMove:

    def __init__(self, power: float = 90., acc: float = 1., max_pp: int = MOVE_MED_PP,
                 move_type: PkmType = PkmType.NORMAL, name: str = None, priority: bool = False,
                 prob=0.0, target=1, recover=0.0, status: PkmStatus = None,
                 stat: PkmStat = PkmStat.ATTACK, stage: int = 0, fixed_damage: float = 0.0,
                 weather: WeatherCondition = None, hazard: PkmEntryHazard = None):
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
        name = "Move(Power=%f, Acc=%f, PP=%d, Type=%s" % (self.power, self.acc, self.pp, self.type.name)
        if self.priority > 0:
            name += ", Priority=%f" % self.priority
        if self.prob > 0.:
            if self.prob < 1.:
                name += ", Prob=%f" % self.prob
            name += "Target=Self" if self.target == 0 else "Target=Opp"
            if self.recover > 0.:
                name += ", Recover=%f" % self.recover
            if self.status != PkmStatus.NONE:
                name += ", Status=%s" % self.status.name
            if self.stage > 0.:
                name += ", Stat=%s, Stage=%d" % (self.stat.name, self.stage)
            if self.fixed_damage > 0.:
                name += ", Fixed=%f" % self.fixed_damage
            if self.weather != self.weather.CLEAR:
                name += ", Weather=%s" % self.weather.name
            if self.hazard is not None:
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
            if self.hazard is not None:
                v.set_entry_hazard(self.hazard, self.target)

    @staticmethod
    def super_effective(t: PkmType) -> PkmType:
        """
        Get a super effective type relative to type t.

        :param t: pokemon type
        :return: a random type that is super effective against pokemon type t
        """
        _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
        s = [index for index, value in enumerate(_t) if value == 2.]
        if not s:
            print('Warning: Empty List!')
            return PkmMove.effective(t)
        return PkmType(random.choice(s))

    @staticmethod
    def non_very_effective(t: PkmType) -> PkmType:
        """
        Get a non very effective type relative to type t.

        :param t: pokemon type
        :return: a random type that is not very effective against pokemon type t
        """
        _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
        s = [index for index, value in enumerate(_t) if value == .5]
        if not s:
            return PkmMove.effective(t)
        return PkmType(random.choice(s))

    @staticmethod
    def effective(t: PkmType) -> PkmType:
        """
        Get a effective type relative to type t.

        :param t: pokemon type
        :return: a random type that is not very effective against pokemon type t
        """
        _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
        s = [index for index, value in enumerate(_t) if value == 1.]
        if not s:
            return PkmType(random.randrange(N_TYPES))
        return PkmType(random.choice(s))


PkmMoveRoster = Set[PkmMove]


class Pkm:
    def __init__(self, p_type: PkmType = PkmType.NORMAL, max_hp: float = MAX_HIT_POINTS,
                 status: PkmStatus = PkmStatus.NONE, move0: PkmMove = PkmMove(), move1: PkmMove = PkmMove(),
                 move2: PkmMove = PkmMove(), move3: PkmMove = PkmMove()):
        self.type: PkmType = p_type
        self.max_hp: float = max_hp
        self.hp: float = max_hp
        self.status: PkmStatus = status
        self.n_turns_asleep: int = 0
        self.moves: List[PkmMove] = [move0, move1, move2, move3]

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

    def __str__(self):
        return 'Pokemon(' + PkmType(self.type).name + ', ' + str(self.hp) + ' HP, ' + PkmStatus(
            self.status).name + ', ' + str(self.moves[0]) + ', ' + str(self.moves[1]) + ', ' + str(
            self.moves[2]) + ', ' + str(self.moves[3]) + ')'


class PkmTemplate:

    def __init__(self, move_roster: PkmMoveRoster, pkm_type: PkmType, max_hp: float):
        self.move_roster: PkmMoveRoster = move_roster
        self.pkm_type: PkmType = pkm_type
        self.max_hp = max_hp

    def get_pkm(self, moves: List[int]) -> Pkm:
        move_list = list(self.move_roster)
        return Pkm(p_type=self.pkm_type, move0=move_list[moves[0]], move1=move_list[moves[1]],
                   move2=move_list[moves[2]], move3=move_list[moves[3]])

    def __str__(self):
        s = 'Pokemon(' + PkmType(self.pkm_type).name + ', ' + str(self.max_hp) + ' HP, '
        for move in self.move_roster:
            s += str(move) + ', '
        return s + ')'


PkmRoster = Set[PkmTemplate]


class PkmTeam:

    def __init__(self, pkms: List[Pkm] = None):
        if pkms is None:
            pkms = [Pkm()]
        self.active: Pkm = pkms.pop(0)
        self.party: List[Pkm] = pkms
        self.stage: List[int] = [0] * N_STATS
        self.confused: bool = False
        self.n_turns_confused: int = 0
        self.entry_hazard: List[int] = [0] * N_ENTRY_HAZARD

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

    class OpponentView:
        def __init__(self, team):
            self.team = team

        def get_n_party(self) -> int:
            return len(self.team.party)

        def get_active(self) -> Tuple[PkmType, float]:
            return self.team.active.type, MAX_HIT_POINTS

        def get_party(self, pos: int = 0) -> Tuple[PkmType, float]:
            return self.team.party[pos].type, MAX_HIT_POINTS

        def encode(self):  # TODO
            """
            Encode opponent team state.

            :return: encoded opponent team state
            """
            e = []
            # e += one_hot(self.team.active.type, N_TYPES)
            # for pos in range(len(self.team.party)):
            #    e += one_hot(self.team.party[pos].type, N_TYPES)
            return e

    class View(OpponentView):

        def get_active(self) -> Tuple[PkmType, float]:
            return self.team.active.type, self.team.active.max_hp

        def get_party(self, pos: int = 0) -> Tuple[PkmType, float]:
            return self.team.party[pos].type, self.team.party[pos].max_hp

    def create_team_view(self) -> Tuple[OpponentView, View]:
        return PkmTeam.OpponentView(self), PkmTeam.View(self)

    def set_pkms(self, team):
        self.active: Pkm = team.active
        self.party: List[Pkm] = team.party

    def select_team(self, selected_pkm: List[int]):
        """
        Get a sub team.

        :param selected_pkm: pkm sub team
        :return: selected sub team
        """
        return PkmTeam(list(map(([self.active] + self.party).__getitem__, selected_pkm)))

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
        Return a list of positions of not fainted pkm in party.

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

        assert -1 <= pos < len(self.party)

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

    def __str__(self):
        party = ''
        for i in range(0, len(self.party)):
            party += str(self.party[i]) + '\n'
        return 'Active:\n%s\nParty:\n%s' % (str(self.active), party)


class MetaData:
    pass
