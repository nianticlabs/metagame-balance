from framework.balance.restriction import DesignConstraints
from framework.competition.Competition import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from framework.datatypes.Objects import PkmRoster
from framework.ecosystem.LeagueEcosystem import Strategy
from framework.ecosystem.VGCEcosystem import VGCEcosystem
from framework.module.MetaGameBalance import MetaGameBalance
from framework.util.Recording import DataDistributionManager


class BalanceEcosystem:

    def __init__(self, c: Competitor, battle_c: Competitor, constraints: DesignConstraints, base_roster: PkmRoster,
                 debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES, ddm: DataDistributionManager = None,
                 n_competitors: int = 16):
        self.__roster = base_roster
        self.__mgb = MetaGameBalance(c, self.__roster, constraints)
        self.__mgb.run()
        self.__vgc: VGCEcosystem = VGCEcosystem(self.__roster, debug, render, n_battles, ddm)
        for competitor in range(n_competitors):
            self.__vgc.register(battle_c)

    def run(self, n_vgc_epochs: int, n_league_epochs: int, strategy: Strategy = Strategy.RANDOM_PAIRING):
        self.__vgc.run(n_vgc_epochs, n_league_epochs, strategy)
        self.__mgb.run()
