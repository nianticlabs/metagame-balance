import copy
import itertools
from abc import ABC, abstractmethod
from typing import Dict, Tuple, List

from math import exp

from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.vgc.balance.archtype import std_move_dist, std_pkm_dist, std_team_dist
from metagame_balance.vgc.datatypes.Objects import PkmTemplate, PkmMove, PkmFullTeam, PkmRoster


class MetaData(ABC):

    @abstractmethod
    def update_with_team(self, team: PkmFullTeam, won: bool):
        pass

    @abstractmethod
    def update_with_delta_roster(self, delta: DeltaRoster):
        pass

    @abstractmethod
    def evaluate(self) -> float:
        pass

    @abstractmethod
    def set_moves_and_pkm(self, roster: PkmRoster) -> None:
        pass

    @abstractmethod
    def update_metadata(self, **kwargs):
        """
        Update the meta data following an iteration of stage 2 optimization
        """
        pass

    @abstractmethod
    def clear_stats(self):
        pass

PkmId = int

class StandardMetaData(MetaData):

    def __init__(self, _max_history_size: int = 1e5, unlimited: bool = False):
        # listings - moves, pkm, teams
        self._moves: List[PkmMove] = []
        self._pkm: List[PkmTemplate] = []
        # global usage rate - moves, pkm
        self._move_usage: Dict[PkmMove, int] = {}
        self._pkm_usage: Dict[PkmId, int] = {}
        # global win rate - moves, pkm
        self._move_wins: Dict[PkmMove, int] = {}
        self._pkm_wins: Dict[PkmId, int] = {}
        # similarity matrix - moves, pkm
        self._d_move: Dict[Tuple[PkmMove, PkmMove], float] = {}
        self._d_pkm: Dict[Tuple[PkmId, PkmId], float] = {}
        self._d_overall_team = 0.0
        # history buffer - moves, pkm, teams
        self._move_history: List[PkmMove] = []
        self._pkm_history: List[PkmId] = []
        self._teammates_history: Dict[Tuple[PkmId, PkmId], int] = {}
        self._team_history: List[Tuple[PkmFullTeam, bool]] = []
        # total usage count - moves, pkm, teams
        self._total_move_usage = 0
        self._total_pkm_usage = 0
        # if meta history size
        self._max_move_history_size: int = _max_history_size * 12
        self._max_pkm_history_size: int = _max_history_size * 3
        self._max_team_history_size: int = _max_history_size
        self._unlimited = unlimited


    def update_metadata(self, **kwargs):
        self.update_with_delta_roster(kwargs['delta'])

    def set_moves_and_pkm(self, roster: PkmRoster):
        self._pkm = list(roster)
        self._moves = []
        for pkm in self._pkm:
            self._moves += list(pkm.move_roster)
        for m0, m1 in itertools.product(self._moves, self._moves):
            self._d_move[(m0, m1)] = std_move_dist(m0, m1)
        self.clear_stats()

    def clear_stats(self):
        for pkm in self._pkm:
            self._pkm_usage[pkm.pkm_id] = 0
            self._pkm_wins[pkm.pkm_id] = 0
        for move in self._moves:
            self._move_usage[move] = 0
            self._move_wins[move] = 0
        for m0, m1 in itertools.product(self._moves, self._moves):
            self._d_move[(m0, m1)] = 0 #std_move_dist(m0, m1)
        for p0, p1 in itertools.product(self._pkm, self._pkm):
            self._d_pkm[(p0.pkm_id, p1.pkm_id)] = std_pkm_dist(p0, p1, move_distance=lambda x, y: self._d_move[x, y])
        self._move_history = []
        self._pkm_history = []
        self._teammates_history = {}
        self._team_history = []
        self._d_overall_team = 0.0
        # total usage count - moves, pkm, teams
        self._total_move_usage = 0
        self._total_pkm_usage = 0

    def update_with_delta_roster(self, delta: DeltaRoster):

        d_move_copy = copy.deepcopy(self._d_move)
        for idx in delta.dp.keys():
            for m_idx in delta.dp[idx].dpm.keys():
                for move_pair in self._d_move.keys():
                    if self._moves[idx * 4 + m_idx] in move_pair:
                        d_move_copy[(move_pair[0], move_pair[1])] = std_move_dist(move_pair[0], move_pair[1])
            for pkm_pair in self._d_pkm.keys():
                if self._pkm[idx].pkm_id in pkm_pair:
                    self._d_pkm[(pkm_pair[0], pkm_pair[1])] = std_pkm_dist(self._pkm[pkm_pair[0]],
                                                                           self._pkm[pkm_pair[1]])
        self._d_move = d_move_copy

    def update_with_team(self, team: PkmFullTeam, won: bool):
        self._team_history.append((team.get_copy(), won))
        # update distance
        for _team in self._team_history:
            self._d_overall_team = std_team_dist(team, _team[0],
                                                 pokemon_distance=lambda x, y: self._d_pkm[x.pkm_id, y.pkm_id])
        # update usages
        for pkm in team.pkm_list:
            self._pkm_usage[pkm.pkm_id] += 1
            if won:
                self._pkm_wins[pkm.pkm_id] += 1
            for move in pkm.moves:
                self._move_usage[move] += 1
                if won:
                    self._move_wins[move] += 1
        for pkm0, pkm1 in itertools.product(team.pkm_list, team.pkm_list):
            if pkm0 != pkm1:
                pair = (pkm0.pkm_id, pkm1.pkm_id)
                if pair not in self._teammates_history.keys():
                    self._teammates_history[pair] = 1
                else:
                    self._teammates_history[pair] += 1
        # update total usages
        self._total_pkm_usage += 3
        self._total_move_usage += 12
        # remove from history past defined maximum length
        if len(self._team_history) > self._max_team_history_size and not self._unlimited:
            team, won = self._team_history.pop(0)
            if won:
                for pkm in team.pkm_list:
                    self._pkm_wins[pkm.pkm_id] -= 1
                    for move in pkm.moves:
                        self._move_wins[move] -= 1
            for pkm0, pkm1 in itertools.product(team.pkm_list, team.pkm_list):
                if pkm0 != pkm1:
                    self._teammates_history[(pkm0.pkm_id, pkm1.pkm_id)] -= 1
            for _team in self._team_history:
                self._d_overall_team -= std_team_dist(team, _team[0], pokemon_distance=lambda x, y: self._d_pkm[x, y])
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

    def get_global_pkm_usage(self, pkm_id: PkmId) -> float:
        return self._pkm_usage[pkm_id] / self._total_pkm_usage

    def get_global_pkm_winrate(self, pkm_id: PkmId) -> float:
        return self._pkm_wins[pkm_id] / self._pkm_usage[pkm_id]

    def get_global_move_usage(self, move: PkmMove) -> float:
        return self._move_usage[move] / self._total_move_usage

    def get_global_move_winrate(self, move: PkmMove) -> float:
        return self._move_wins[move] / self._move_usage[move]

    def get_pair_usage(self, pair: Tuple[PkmId, PkmId]) -> float:
        if pair not in self._teammates_history.keys():
            return 0.0
        return self._teammates_history[pair] / self._pkm_usage[pair[0]]

    def get_team(self, t) -> Tuple[PkmFullTeam, bool]:
        return self._team_history[t][0], self._team_history[t][1]

    def get_n_teams(self) -> int:
        return len(self._team_history)

    def evaluate(self) -> float:
        d = [0., 0., 0., 0., 0.]
        # Overall number of different Pkm (templates).
        for pkm0, pkm1 in itertools.product(self._pkm, self._pkm):
            d[0] += - self._pkm_usage[pkm1.pkm_id] * exp(-self._d_pkm[(pkm0.pkm_id, pkm1.pkm_id)]) + 1
        d[0] /= 2
        # Overall number of different Pkm moves.
        for move0, move1 in itertools.product(self._moves, self._moves):
            d[1] += - self._move_usage[move1] * exp(-self._d_move[(move0, move1)]) + 1
        d[1] /= 2
        # Overall number of different Pkm teams.
        d[2] = self._d_overall_team
        for team, win in self._team_history:
            # Difference over moves on same Pkm.
            moves = []
            for pkm in team.pkm_list:
                moves.extend(pkm.moves)
            for move0, move1 in itertools.product(moves, moves):
                d[3] += - exp(-self._d_move[(move0, move1)]) + 1
            # Difference over Pkm on same team.
            for pkm0, pkm1 in itertools.product(team.pkm_list, team.pkm_list):
                d[4] += - exp(-self._d_pkm[(pkm0.pkm_id, pkm1.pkm_id)]) + 1
        d[3] /= 2
        d[4] /= 2
        return sum(d)
