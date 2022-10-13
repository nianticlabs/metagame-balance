from enum import Enum
from random import shuffle
from typing import List, Tuple

from elo import rate_1vs1

from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.competition.BattleMatch import BattleMatch
from metagame_balance.vgc.datatypes.Constants import DEFAULT_MATCH_N_BATTLES, DEFAULT_TEAM_SIZE


class Strategy(Enum):
    RANDOM_PAIRING = 0
    ELO_PAIRING = 1


class BattleEcosystem:

    def __init__(self, meta_data: MetaData, debug=False, render=False, n_battles=DEFAULT_MATCH_N_BATTLES,
                 pairings_strategy: Strategy = Strategy.RANDOM_PAIRING, update_meta=False,
                 full_team_size: int = DEFAULT_TEAM_SIZE):
        self.meta_data = meta_data
        self.competitors: List[CompetitorManager] = []
        self.debug = debug
        self.render = render
        self.n_battles = n_battles
        self.full_team_size = full_team_size
        self.pairings_strategy = pairings_strategy
        self.update_meta = update_meta
        self.team_wins = {}

    def register(self, cm: CompetitorManager):
        if cm not in self.competitors:
            self.competitors.append(cm)
            self.team_wins[cm] = 0

    def unregister(self, cm: CompetitorManager):
        self.competitors.remove(cm)
        del self.team_wins[cm]

    def run(self, n_epochs: int):
        for _ in range(n_epochs):
            self.__run_matches(self.__schedule_matches())

    def __schedule_matches(self) -> List[Tuple[CompetitorManager, CompetitorManager]]:
        n_matches = len(self.competitors) // 2
        matches: List[Tuple[CompetitorManager, CompetitorManager]] = []
        if self.pairings_strategy == Strategy.RANDOM_PAIRING:
            shuffle(self.competitors)
        elif self.pairings_strategy == Strategy.ELO_PAIRING:
            sorted(self.competitors, key=lambda x: x.elo)
        for i in range(n_matches):
            matches.append((self.competitors[2 * i], self.competitors[2 * i + 1]))
        return matches

    def __run_matches(self, pairs: List[Tuple[CompetitorManager, CompetitorManager]]):
        for pair in pairs:
            cm0, cm1 = pair
            match = BattleMatch(cm0, cm1, self.n_battles, self.debug, self.render, meta_data=self.meta_data,
                                update_meta=self.update_meta, full_team_size=self.full_team_size)
            match.run()
            if match.winner() == 0:
                cm0.elo, cm1.elo = rate_1vs1(cm0.elo, cm1.elo)
                self.team_wins[cm0] += 1
            elif match.winner() == 1:
                self.team_wins[cm1] += 1
                cm1.elo, cm0.elo = rate_1vs1(cm1.elo, cm0.elo)

    def clear_wins(self):
        for t in self.team_wins.keys():
            self.team_wins[t] = 0

    def get_team_wins(self, cm: CompetitorManager):
        return self.team_wins[cm]
