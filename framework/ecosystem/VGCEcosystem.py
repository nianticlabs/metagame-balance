from typing import List
from framework.DataConstants import DEFAULT_MATCH_N_BATTLES
from framework.DataObjects import PkmRoster
from framework.competition.CompetitionObjects import Competitor
from framework.ecosystem import CompetitorManager
from framework.ecosystem.LeagueEcosystem import LeagueEcosystem, Strategy
from framework.util.Recording import GamePlayRecorder


class VGCEcosystem:

    def __init__(self, roster: PkmRoster, debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES,
                 rec: GamePlayRecorder = None):
        self.__roster = roster
        self.__competitors: List[CompetitorManager] = []
        self.__league: LeagueEcosystem = LeagueEcosystem(debug, render, n_battles, rec)

    def register(self, c: Competitor):
        if c not in list(map(lambda x: x.competitor, self.__competitors)):
            cm = CompetitorManager(c, self.__roster)
            cm.tbp.run()
            c.team = cm.tbp.output()
            self.__competitors.append(cm)

    def run(self, n_epochs: int, n_league_epochs: int, strategy: Strategy = Strategy.RANDOM_PAIRING):
        epoch = 0
        while epoch < n_epochs:
            for cm in self.__competitors:
                if cm.competitor.want_to_change_team:
                    cm.tbp.run()
                    cm.competitor.team = cm.tbp.output()
            self.__league.run(n_league_epochs, strategy)
            epoch += 1
