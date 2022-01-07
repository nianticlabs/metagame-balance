from typing import List

from framework.competition import CompetitorManager
from framework.competition.Competition import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from framework.datatypes.Objects import PkmRoster
from framework.ecosystem.LeagueEcosystem import LeagueEcosystem, Strategy
from framework.util.Recording import DataDistributionManager


class VGCEcosystem:

    def __init__(self, roster: PkmRoster, debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES,
                 ddm: DataDistributionManager = None):
        self.roster = roster
        self.competitors: List[CompetitorManager] = []
        self.league: LeagueEcosystem = LeagueEcosystem(debug, render, n_battles, ddm)

    def register(self, c: Competitor):
        if c not in list(map(lambda x: x.competitor, self.competitors)):
            cm = CompetitorManager(c)
            cm.new_team_building_process(self.roster)
            cm.tbp.run()
            cm.team = cm.tbp.output()
            self.competitors.append(cm)
            self.league.register(cm)

    def run(self, n_epochs: int, n_league_epochs: int, strategy: Strategy = Strategy.RANDOM_PAIRING):
        epoch = 0
        while epoch < n_epochs:
            for cm in self.competitors:
                cm.tbp.run()
                cm.competitor.team = cm.tbp.output()
            print("LEAGUE")
            self.league.run(n_league_epochs, strategy)
            epoch += 1
