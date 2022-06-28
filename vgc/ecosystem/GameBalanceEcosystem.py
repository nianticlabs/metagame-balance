from copy import deepcopy
from typing import List

from vgc.balance.meta import MetaData
from vgc.balance.restriction import VGCDesignConstraints
from vgc.competition import CompetitorManager
from vgc.competition.Competition import Competitor
from vgc.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from vgc.datatypes.Objects import PkmRoster, get_pkm_roster_view
from vgc.ecosystem.BattleEcosystem import Strategy
from vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem


class GameBalanceEcosystem:

    def __init__(self, competitor: Competitor, surrogate_agent: List[CompetitorManager],
                 constraints: VGCDesignConstraints, base_roster: PkmRoster, meta_data: MetaData, debug=False,
                 render=False, n_battles=DEFAULT_MATCH_N_BATTLES, strategy: Strategy = Strategy.RANDOM_PAIRING):
        self.c = competitor
        self.constraints = constraints
        self.meta_data = meta_data
        self.rewards = []
        self.vgc: ChampionshipEcosystem = ChampionshipEcosystem(base_roster, meta_data, debug, render, n_battles,
                                                                strategy=strategy)
        for c in surrogate_agent:
            self.vgc.register(c)

    def run(self, n_epochs, n_vgc_epochs: int, n_league_epochs: int) -> List:
        epoch = 0
        while epoch < n_epochs:
            self.meta_data.clear_stats()  #consider doing it inside the league as well! or
            self.vgc.run(n_vgc_epochs, n_league_epochs)
            self.rewards += [self.meta_data.evaluate()]
            delta_roster = self.c.balance_policy.get_action((self.vgc.roster, self.meta_data,
                                                             self.constraints))
            copy_roster = deepcopy(self.vgc.roster)
            delta_roster.apply(copy_roster)
            violated_rules = self.constraints.check_every_rule(copy_roster)
            if len(violated_rules) == 0:
                delta_roster.apply(self.vgc.roster)
                self.meta_data.update_with_delta_roster(delta_roster)
            else:
                raise AssertionError
            print('-' * 30 + "VGC EPOCH " + str(epoch) + " DONE" + '-' * 30)
            for pkm in self.vgc.roster:
                print(pkm)
                for move in pkm.move_roster:
                    print(move.power, move.acc, move.max_pp)
            epoch += 1
