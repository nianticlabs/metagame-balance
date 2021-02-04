from copy import deepcopy

from framework.DataConstants import DEFAULT_MATCH_N_BATTLES
from framework.DataObjects import DesignConstraints, PkmRoster
from framework.competition.CompetitionObjects import Competitor
from framework.ecosystem.LeagueEcosystem import Strategy
from framework.ecosystem.VGCEcosystem import VGCEcosystem
from framework.module.MetaGameBalance import MetaGameBalance
from framework.util.Recording import GamePlayRecorder


class BalanceEcosystem:

    def __init__(self, c: Competitor, battle_c: Competitor, constraints: DesignConstraints, debug=False, render=True,
                 n_battles=DEFAULT_MATCH_N_BATTLES, rec: GamePlayRecorder = None, n_competitors: int = 16):
        self.__roster = PkmRoster()
        self.__mgb = MetaGameBalance(c, self.__roster, constraints)
        self.__mgb.run()
        self.__vgc: VGCEcosystem = VGCEcosystem(self.__roster, debug, render, n_battles, rec)
        for competitor in range(n_competitors):
            self.__vgc.register(deepcopy(battle_c))

    def run(self, n_vgc_epochs: int, n_league_epochs: int, strategy: Strategy = Strategy.RANDOM_PAIRING):
        self.__vgc.run(n_vgc_epochs, n_league_epochs, strategy)
        self.__mgb.run()

