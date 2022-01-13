from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, List

from framework.balance.archtype import TeamArchtype, standard_move_distance, standard_pkm_distance
from framework.datatypes.Objects import PkmTemplate, PkmMove


class MetaData(ABC):

    @abstractmethod
    def evaluate(self) -> float:
        pass


class StandardMetaData(MetaData):

    def __init__(self, _max_history_size: int = 1e5, unlimited: bool = False):
        # listings - moves, pkm, teams
        self._moves: List[PkmMove] = []
        self._pkm: List[PkmTemplate] = []
        self._teams: Set[TeamArchtype] = set()
        # global usage rate - moves, pkm
        self._move_usage: Dict[PkmMove, int] = {}
        self._pkm_usage: Dict[PkmTemplate, int] = {}
        self._team_usage: Dict[TeamArchtype, int] = {}
        # similarity matrix - moves, pkm
        self._d_move: Dict[Tuple[PkmMove, PkmMove], float] = {}
        self._d_pkm: Dict[Tuple[PkmTemplate, PkmTemplate], float] = {}
        # win rate history - teams
        self._victory_matrix: Dict[Tuple[TeamArchtype, TeamArchtype], int] = {}
        # history buffer - moves, pkm, teams
        self._move_history: List[PkmMove] = []
        self._pkm_history: List[PkmTemplate] = []
        self._team_history: List[TeamArchtype] = []
        # total usage count - moves, pkm, teams
        self._total_move_usage = 0
        self._total_pkm_usage = 0
        self._total_team_usage = 0
        # if meta history size
        self._max_move_history_size: int = _max_history_size * 24
        self._max_pkm_history_size: int = _max_history_size * 6
        self._max_team_history_size: int = _max_history_size * 2
        self._unlimited = unlimited

    def set_moves_pkm(self, moves: List[PkmMove], pkm: List[PkmTemplate]):
        self._moves = moves
        self._pkm = pkm
        for m0, m1 in zip(self._moves, self._moves):
            self._d_move[(m0, m1)] = standard_move_distance(m0, m1)
        for p0, p1 in zip(self._pkm, self._pkm):
            self._d_pkm[(p0, p1)] = standard_pkm_distance(p0, p1, move_distance=lambda x, y: self._d_move[x, y])

    def adapt_moves_pkm(self, moves: List[PkmMove], pkms: List[PkmTemplate]):
        for move in moves:
            for move_pair in self._d_move.keys():
                if move in move_pair:
                    self._d_move[(move_pair[0], move_pair[1])] = standard_move_distance(move_pair[0], move_pair[1])
        for pkm in pkms:
            for pkm_pair in self._d_pkm.keys():
                if pkm in pkm_pair:
                    self._d_pkm[(pkm_pair[0], pkm_pair[1])] = standard_pkm_distance(pkm_pair[0], pkm_pair[1])

    def set_archtype(self, archtype: TeamArchtype):
        if archtype not in self._teams:
            for existing in self._teams:
                self._victory_matrix[(archtype, existing)] = 0
                self._victory_matrix[(existing, archtype)] = 0
            self._team_usage[archtype] = 0
            self._teams.add(archtype)

    def update(self, winner: TeamArchtype, loser: TeamArchtype):
        # update win rate
        self._victory_matrix[(winner, loser)] += 1
        # update usages
        for pkm in winner:
            self._pkm_usage[pkm] += 1
            for move in pkm.moves:
                self._move_usage[move] += 1
        for pkm in loser:
            self._pkm_usage[pkm] += 1
            for move in pkm.moves:
                self._move_usage[move] += 1
        self._team_usage[winner] += 1
        self._team_usage[loser] += 1
        # update total usages
        self._total_move_usage += 24
        self._total_pkm_usage += 6
        self._total_team_usage += 2
        # update history
        self._team_history.append(winner)
        self._team_history.append(loser)
        # remove from history past defined maximum length
        if len(self._team_history) > self._max_team_history_size and not self._unlimited:
            old_achtype0 = self._team_history.pop(0)
            old_achtype1 = self._team_history.pop(0)
            self._team_usage[old_achtype0] -= 1
            self._team_usage[old_achtype1] -= 1
            self._total_team_usage -= 2
            if self._team_usage[old_achtype0] == 0:
                self._remove_archtype(old_achtype0)
            if self._team_usage[old_achtype1] == 0:
                self._remove_archtype(old_achtype1)

    def _remove_archtype(self, archtype: TeamArchtype):
        self._teams.remove(archtype)
        self._team_usage.pop(archtype)
        for existing in self._teams:
            self._victory_matrix.pop((archtype, existing))
            self._victory_matrix.pop((existing, archtype))

    def get_winrate(self, archtype: TeamArchtype, opponent: TeamArchtype) -> float:
        if archtype == opponent:
            return 0.5
        victories = self._victory_matrix[(archtype, opponent)]
        losses = self._victory_matrix[(opponent, archtype)]
        return victories / max((victories + losses), 1)

    def get_usagerate(self, archtype: TeamArchtype):
        return self._team_usage[archtype] / self._total_team_usage

    def get_pkm_usagerate(self, pkm: PkmTemplate):
        return self._pkm_usage[pkm] / self._total_pkm_usage

    def evaluate(self) -> float:
        # TODO
        return 0.0
