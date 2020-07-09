import random
from enum import IntEnum
import numpy as np

from Engine.PkmConstants import MAX_HIT_POINTS, TYPE_CHART_MULTIPLIER, MOVE_MED_PP
from typing import List, Tuple

# Pokemon Typing
from Util.Encoding import one_hot


class PkmType(IntEnum):
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


N_TYPES = len(list(map(int, PkmType)))


# Battle Weather conditions
class WeatherCondition(IntEnum):
    CLEAR = 0
    SUNNY = 1
    RAIN = 2
    SANDSTORM = 3
    HAIL = 4


N_WEATHER = len(list(map(int, WeatherCondition)))


# Pokemon battle status
class PkmStatus(IntEnum):
    NONE = 0
    PARALYZED = 1
    POISONED = 2
    CONFUSED = 3
    SLEEP = 4
    FROZEN = 5
    BURNED = 6


N_STATUS = len(list(map(int, PkmStatus)))


# Pokemon battle stats
class PkmStat(IntEnum):
    ATTACK = 0
    DEFENSE = 1
    SPEED = 2


N_STATS = len(list(map(int, PkmStat)))
MAX_STAGE = 5
MIN_STAGE = -5
N_STAGES = MAX_STAGE - MIN_STAGE + 1


# Pokemon battle stats
class PkmEntryHazard(IntEnum):
    SPIKES = 0


N_ENTRY_HAZARD = len(list(map(int, PkmEntryHazard)))
N_HAZARD_STAGES = 3


def null_effect(view):
    pass


class PkmMove:

    def __init__(self, power: float = 90., acc: float = 1., max_pp: int = MOVE_MED_PP,
                 move_type: PkmType = PkmType.NORMAL, name: str = "", effect=null_effect, priority: bool = False):
        """
        Pokemon move data structure. Special moves have power = 0.

        :param power: pokemon move power
        :param move_type: pokemon move type
        """
        self.power = power
        self.acc = acc
        self.max_pp = max_pp
        self.pp = max_pp
        self.type = move_type
        self.name = name
        self.effect = effect
        self.priority = priority

    def __str__(self):
        return "Move(" + str(self.power) + ", " + str(self.acc) + ", " + str(self.pp) + ", " + self.type.name + ", " + str(self.priority) + ")" if not self.name else self.name

    def reset(self):
        self.pp = self.max_pp

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
        return random.choice(s)

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
        return random.choice(s)

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
            return random.randrange(N_TYPES)
        return random.choice(s)


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
        return self.status == PkmStatus.SLEEP and np.random.uniform(0, 1) <= 0.33

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

        def encode(self):
            """
            Encode opponent team state.

            :return: encoded opponent team state
            """
            e = []
            e += one_hot(self.team.active.type, N_TYPES)
            for pos in range(len(self.team.party)):
                e += one_hot(self.team.party[pos].type, N_TYPES)
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
