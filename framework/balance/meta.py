from abc import ABC, abstractmethod
from typing import Dict, Tuple, List

from framework.balance import DeltaRoster
from framework.balance.archtype import standard_move_distance, standard_pkm_distance
from framework.datatypes.Objects import PkmTemplate, PkmMove, PkmFullTeam


class MetaData(ABC):

    @abstractmethod
    def update_with_team(self, team: PkmFullTeam, won: bool):
        pass

    @abstractmethod
    def update_with_delta_roster(self, delta: DeltaRoster):
        pass

    @abstractmethod
    def get_global_pkm_usage(self, pkm: PkmTemplate) -> float:
        pass

    @abstractmethod
    def get_global_pkm_winrate(self, pkm: PkmTemplate) -> float:
        pass

    @abstractmethod
    def get_global_move_usage(self, move: PkmMove) -> float:
        pass

    @abstractmethod
    def evaluate(self) -> float:
        pass


class StandardMetaData(MetaData):

    def __init__(self, _max_history_size: int = 1e5, unlimited: bool = False):
        # listings - moves, pkm, teams
        self._moves: List[PkmMove] = []
        self._pkm: List[PkmTemplate] = []
        # global usage rate - moves, pkm
        self._move_usage: Dict[PkmMove, int] = {}
        self._pkm_usage: Dict[PkmTemplate, int] = {}
        self._pkm_wins: Dict[PkmTemplate, int] = {}
        # similarity matrix - moves, pkm
        self._d_move: Dict[Tuple[PkmMove, PkmMove], float] = {}
        self._d_pkm: Dict[Tuple[PkmTemplate, PkmTemplate], float] = {}
        # history buffer - moves, pkm, teams
        self._move_history: List[PkmMove] = []
        self._pkm_history: List[PkmTemplate] = []
        self._team_history: List[Tuple[PkmFullTeam, bool]] = []
        # total usage count - moves, pkm, teams
        self._total_move_usage = 0
        self._total_pkm_usage = 0
        # if meta history size
        self._max_move_history_size: int = _max_history_size * 12
        self._max_pkm_history_size: int = _max_history_size * 3
        self._max_team_history_size: int = _max_history_size
        self._unlimited = unlimited

    def set_moves_pkm(self, moves: List[PkmMove], pkm: List[PkmTemplate]):
        self._moves = moves
        self._pkm = pkm
        for m0, m1 in zip(self._moves, self._moves):
            self._d_move[(m0, m1)] = standard_move_distance(m0, m1)
        for p0, p1 in zip(self._pkm, self._pkm):
            self._d_pkm[(p0, p1)] = standard_pkm_distance(p0, p1, move_distance=lambda x, y: self._d_move[x, y])

    def update_with_delta_roster(self, delta: DeltaRoster):
        for idx in delta.dp.keys():
            for m_idx in delta.dp[idx].dpm.keys():
                for move_pair in self._d_move.keys():
                    if self._moves[idx * 4 + m_idx] in move_pair:
                        self._d_move[(move_pair[0], move_pair[1])] = standard_move_distance(move_pair[0], move_pair[1])
            for pkm_pair in self._d_pkm.keys():
                if self._pkm[idx] in pkm_pair:
                    self._d_pkm[(pkm_pair[0], pkm_pair[1])] = standard_pkm_distance(pkm_pair[0], pkm_pair[1])

    def update_with_team(self, team: PkmFullTeam, won: bool):
        self._team_history.append((team.get_copy(), won))
        # update usages
        for pkm in team.pkm_list:
            self._pkm_usage[pkm] += 1
            if won:
                self._pkm_wins[pkm] += 1
            for move in pkm.moves:
                self._move_usage[move] += 1
        # update total usages
        self._total_pkm_usage += 3
        self._total_move_usage += 12
        # remove from history past defined maximum length
        if len(self._team_history) > self._max_team_history_size and not self._unlimited:
            team, won = self._team_history.pop(0)
            if won:
                for pkm in team.pkm_list:
                    self._pkm_wins[pkm] -= 1
        if len(self._pkm_history) > self._max_pkm_history_size and not self._unlimited:
            for _ in range(3):
                old_pkm = self._pkm_history.pop(0)
                self._pkm_usage[old_pkm] -= 1
            self._total_pkm_usage -= 3
        if len(self._move_history) > self._max_move_history_size and not self._unlimited:
            for _ in range(12):
                old_move = self._move_history.pop(0)
                self._move_usage[old_move] -= 1
            self._total_move_usage -= 12

    def get_global_pkm_usage(self, pkm: PkmTemplate) -> float:
        return self._pkm_usage[pkm] / self._total_pkm_usage

    def get_global_pkm_winrate(self, pkm: PkmTemplate) -> float:
        return self._pkm_wins[pkm] / self._pkm_usage[pkm]

    def get_global_move_usage(self, move: PkmMove) -> float:
        return self._move_usage[move] / self._total_move_usage

    def evaluate(self) -> float:
        return 0.0
