from typing import List

from framework.balance.meta import MetaData
from framework.balance.restriction import VGCDesignConstraints
from framework.competition import CompetitorManager
from framework.competition.Competition import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from framework.datatypes.Objects import PkmRoster, get_pkm_roster_view
from framework.ecosystem.BattleEcosystem import Strategy
from framework.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem


class GameBalanceEcosystem:

    def __init__(self, competitor: Competitor, surrogate_agent: List[CompetitorManager],
                 constraints: VGCDesignConstraints, base_roster: PkmRoster, meta_data: MetaData, debug=False,
                 render=False, n_battles=DEFAULT_MATCH_N_BATTLES, strategy: Strategy = Strategy.RANDOM_PAIRING):
        self.c = competitor
        self.constraints = constraints
        self.meta_data = meta_data
        self.accumulated_points = 0.0
        self.vgc: ChampionshipEcosystem = ChampionshipEcosystem(base_roster, meta_data, debug, render, n_battles,
                                                                strategy=strategy)
        for c in surrogate_agent:
            self.vgc.register(c)

    def run(self, n_epochs, n_vgc_epochs: int, n_league_epochs: int):
        epoch = 0
        while epoch < n_epochs:
            self.vgc.run(n_vgc_epochs, n_league_epochs)
            self.accumulated_points += self.meta_data.evaluate()
            delta_roster = self.c.balance_policy.get_action((get_pkm_roster_view(self.vgc.roster), self.meta_data,
                                                             self.constraints))
            delta_roster.apply(self.vgc.roster)
            violated_rules = self.constraints.check_every_rule(self.vgc.roster)
            if len(violated_rules) == 0:
                pass
                # TODO update meta with deltas
            epoch += 1
