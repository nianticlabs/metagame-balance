from typing import List
from framework.DataConstants import DEFAULT_MATCH_N_BATTLES
from framework.competition.CompetitionObjects import Competitor
from framework.module.BattlePhase import BattlePhase
from framework.module.SelectionPhase import SelectionPhase
from framework.util.Recording import GamePlayRecorder


class LeagueEcosystem:

    def __init__(self, debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES, rec: GamePlayRecorder = None):
        self.__competitors: List[Competitor] = []
        self.__debug = debug
        self.__render = render
        self.__n_battles = n_battles
        self.__rec = rec

    def register(self, c: Competitor):
        if c not in self.__competitors:
            self.__competitors.append(c)

    def unregister(self, c: Competitor):
        self.__competitors.remove(c)

    def schedule(self):  # TODO
        pass

    def run_epoch(self):  # TODO
        pass

    def __run_match(self, c0: Competitor, c1: Competitor):
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
