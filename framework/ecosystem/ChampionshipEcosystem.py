from typing import List

from framework.balance.meta import MetaData
from framework.competition import CompetitorManager, legal_team
from framework.competition.Competition import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from framework.datatypes.Objects import PkmRoster, TeamValue, get_pkm_roster_view
from framework.ecosystem.BattleEcosystem import BattleEcosystem, Strategy
from framework.util.generator.PkmTeamGenerators import RandomGeneratorRoster


class NullTeamValue(TeamValue):

    def compare_to(self, value) -> int:
        return 0


null_team_value = NullTeamValue()


class ChampionshipEcosystem:

    def __init__(self, roster: PkmRoster, meta_data: MetaData, debug=False, render=True,
                 n_battles=DEFAULT_MATCH_N_BATTLES, strategy: Strategy = Strategy.RANDOM_PAIRING):
        self.meta_data = meta_data
        self.roster = roster
        self.roster_view = get_pkm_roster_view(self.roster)
        self.rand_gen = RandomGeneratorRoster(self.roster)
        self.competitors: List[CompetitorManager] = []
        self.league: BattleEcosystem = BattleEcosystem(self.meta_data, debug, render, n_battles, strategy)

    def register(self, c: Competitor):
        if c not in list(map(lambda x: x.competitor, self.competitors)):
            cm = CompetitorManager(c)
            self.__set_new_team(cm)
            self.competitors.append(cm)
            self.league.register(cm)

    def run(self, n_epochs: int, n_league_epochs: int):
        epoch = 0
        while epoch < n_epochs:
            print("TEAM UPDATES")
            for cm in self.competitors:
                self.__set_new_team(cm)
            print("LEAGUE")
            self.league.run(n_league_epochs)
            epoch += 1

    def __set_new_team(self, cm: CompetitorManager):
        try:
            if cm.team is None:
                value = null_team_value
            else:
                value = cm.competitor.team_valuator_policy().get_action((cm.team, self.meta_data))
        except:
            value = null_team_value
        try:
            cm.team = cm.competitor.team_builder_policy.get_action((self.meta_data, cm.team, self.roster_view, value))
            if not legal_team(cm.team, self.roster):
                cm.team = self.rand_gen.get_team()
        except:
            cm.team = cm.team
