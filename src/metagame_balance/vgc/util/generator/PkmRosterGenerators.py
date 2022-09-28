import random
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List

from metagame_balance.vgc.competition.StandardPkmMoves import STANDARD_MOVE_ROSTER
from metagame_balance.vgc.competition import STANDARD_TOTAL_POINTS, get_move_points
from metagame_balance.vgc.datatypes.Constants import BASE_HIT_POINTS, DEFAULT_ROSTER_SIZE, DEFAULT_N_MOVES_PKM, MAX_HIT_POINTS, \
    MIN_HIT_POINTS
from metagame_balance.vgc.datatypes.Objects import PkmMoveRoster, PkmRoster, PkmMove, PkmTemplate
from metagame_balance.vgc.datatypes.Types import PkmType
from metagame_balance.vgc.util.generator.PkmTeamGenerators import LIST_OF_TYPES


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
        moves = random.sample(list(filter(lambda _m: _m.type == self.pkm_type, base_move_roster)), 1)
        for m in moves:
            base_move_roster.remove(m)
        move_roster: List[PkmMove] = moves
        for _ in range(self.n_moves_pkm - 1):
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
            move_roster = RandomMoveRosterGenerator(self.base_move_roster, p_type, self.n_moves_pkm).gen_roster()
            points = 0
            for move in move_roster:
                points += get_move_points(move)
            max_hp: float = BASE_HIT_POINTS + 30. * (STANDARD_TOTAL_POINTS - points)
            if max_hp > MAX_HIT_POINTS:
                max_hp = MAX_HIT_POINTS
            if max_hp < MIN_HIT_POINTS:
                max_hp = MIN_HIT_POINTS
            roster.append(PkmTemplate(move_roster, p_type, max_hp, i))
        return set(roster)
