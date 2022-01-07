from framework.balance.meta import MetaData
from framework.balance.restriction import DesignConstraints
from framework.competition.Competition import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from framework.datatypes.Objects import PkmRoster
from framework.ecosystem.BattleEcosystem import Strategy
from framework.ecosystem.VGCEcosystem import VGCEcosystem


class GameBalanceEcosystem:

    def __init__(self, c: Competitor, battle_c: Competitor, constraints: DesignConstraints, base_roster: PkmRoster,
                 meta_data: MetaData, debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES,
                 n_competitors: int = 16):
        self.roster = base_roster
        self.mgb = MetaGameBalance(c, self.roster, meta_data, constraints)
        self.mgb.run()
        self.vgc: VGCEcosystem = VGCEcosystem(self.roster, meta_data, debug, render, n_battles)
        for competitor in range(n_competitors):
            self.vgc.register(battle_c)

    def run(self, n_vgc_epochs: int, n_league_epochs: int, strategy: Strategy = Strategy.RANDOM_PAIRING):
        self.vgc.run(n_vgc_epochs, n_league_epochs, strategy)
        self.mgb.run()