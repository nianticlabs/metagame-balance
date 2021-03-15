import random
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List

from framework.DataConstants import MIN_HIT_POINTS, MOVE_POWER_MIN, DEFAULT_ROSTER_SIZE, DEFAULT_N_MOVES_PKM
from framework.DataObjects import PkmMoveRoster, PkmRoster, PkmMove, PkmTemplate
from framework.DataTypes import PkmType
from framework.StandardPkmMoves import STANDARD_MOVE_ROSTER
from framework.util.PkmTeamGenerators import LIST_OF_TYPES, DELTA_HIT_POINTS, DELTA_MOVE_POWER


class MoveRosterGenerator(ABC):

    def gen_roster(self) -> PkmMoveRoster:
        pass


class RandomMoveRosterGenerator(MoveRosterGenerator):

    def __init__(self, base_roster=None, pkm_type: PkmType = PkmType.NORMAL, n_moves_pkm: int = DEFAULT_N_MOVES_PKM):
        if base_roster is None:
            base_roster = set(STANDARD_MOVE_ROSTER)
        self.base_roster = base_roster
        self.pkm_type = pkm_type
        self.n_moves_pkm = n_moves_pkm

    def gen_roster(self) -> PkmMoveRoster:
        base_move_roster = deepcopy(self.base_roster)
        moves = random.sample(list(filter(lambda _m: _m.type == self.pkm_type, base_move_roster)), 2)
        for m in moves:
            base_move_roster.remove(m)
        move_roster: List[PkmMove] = moves
        for _ in range(self.n_moves_pkm - 1):
            if random.random() < .2:
                m_type: PkmType = random.choice(LIST_OF_TYPES)
                m_power: float = round(random.random() * DELTA_MOVE_POWER + MOVE_POWER_MIN)
                move = PkmMove(power=m_power, move_type=m_type)
            else:
                move = random.choice(list(base_move_roster))
                base_move_roster.remove(move)
            move_roster.append(move)
        return set(move_roster)


class PkmRosterGenerator(ABC):

    @abstractmethod
    def gen_roster(self) -> PkmRoster:
        pass


class RandomPkmRosterGenerator(PkmRosterGenerator):

    def __init__(self, base_move_roster=None, n_moves_pkm: int = DEFAULT_N_MOVES_PKM,
                 roster_size: int = DEFAULT_ROSTER_SIZE):
        if base_move_roster is None:
            base_move_roster = set(STANDARD_MOVE_ROSTER)
        self.base_move_roster: PkmMoveRoster = base_move_roster
        self.n_moves_pkm = n_moves_pkm
        self.roster_size = roster_size

    def gen_roster(self) -> PkmRoster:
        """
        Generate a random pokemon roster that follows the generator specifications.

        :return: a random pokemon roster.
        """
        roster: List[PkmTemplate] = []
        for i in range(self.roster_size):
            p_type: PkmType = random.choice(LIST_OF_TYPES)
            max_hp: float = round(random.random() * DELTA_HIT_POINTS + MIN_HIT_POINTS)
            move_roster = RandomMoveRosterGenerator(self.base_move_roster, p_type, self.n_moves_pkm).gen_roster()
            roster.append(PkmTemplate(move_roster, p_type, max_hp))
        return set(roster)
