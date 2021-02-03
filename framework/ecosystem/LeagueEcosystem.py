from enum import Enum
from random import shuffle

from elo import rate_1vs1
from typing import List, Tuple
from framework.DataConstants import DEFAULT_MATCH_N_BATTLES
from framework.ecosystem import CompetitorManager
from framework.module.BattlePhase import BattlePhase
from framework.module.SelectionPhase import SelectionPhase
from framework.util.Recording import GamePlayRecorder


class Strategy(Enum):
    RANDOM_PAIRING = 0
    ELO_PAIRING = 1


class LeagueEcosystem:

    def __init__(self, debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES, rec: GamePlayRecorder = None):
        self.__competitors: List[CompetitorManager] = []
        self.__debug = debug
        self.__render = render
        self.__n_battles = n_battles
        self.__rec = rec

    def register(self, cm: CompetitorManager):
        if cm not in self.__competitors:
            self.__competitors.append(cm)

    def unregister(self, cm: CompetitorManager):
        self.__competitors.remove(cm)

    def run(self, n_epochs: int, strategy: Strategy):
        epoch = 0
        n_matches = len(self.__competitors) // 2
        while epoch < n_epochs:
            # schedule matches
            matches: List[Tuple[CompetitorManager, CompetitorManager]] = []
            if strategy == Strategy.RANDOM_PAIRING:
                shuffle(self.__competitors)
            elif strategy == Strategy.ELO_PAIRING:
                sorted(self.__competitors, key=lambda x: x.elo)
            for i in range(n_matches):
                matches.append((self.__competitors[2 * i], self.__competitors[2 * i + 1]))
            # run matches
            for match in matches:
                self.__run_match(match[0], match[1])
            del matches
            epoch += 1

    def __run_match(self, cm0: CompetitorManager, cm1: CompetitorManager):
        c0 = cm0.competitor
        c1 = cm1.competitor
        c0.reset()
        c1.reset()
        c0.team.hide()
        c1.team.hide()
        sp0 = SelectionPhase(c0, c1.team)
        sp1 = SelectionPhase(c1, c0.team)
        team0, prediction0 = sp0.output()  # output empty containers
        team1, prediction1 = sp0.output()  # output empty containers
        bp = BattlePhase(c0, c1, team0, team1, prediction0, prediction1, debug=self.__debug, render=self.__render,
                         n_battles=self.__n_battles, rec=self.__rec)
        for i in range(self.__n_battles):
            sp0.run()
            sp1.run()
            bp.run()
        if bp.winner == 0:
            cm0.elo, cm1.elo = rate_1vs1(cm0.elo, cm1.elo)
        elif bp.winner == 1:
            cm1.elo, cm0.elo = rate_1vs1(cm1.elo, cm0.elo)
