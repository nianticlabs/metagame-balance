import random
from abc import ABC, abstractmethod
from typing import List, Optional

from framework.balance.meta import MetaData
from framework.behaviour.TeamValuators import NullTeamValuator
from framework.competition import CompetitorManager
from framework.competition.BattleMatch import BattleMatch
from framework.competition.Competitor import Competitor
from framework.datatypes.Objects import PkmRoster, get_pkm_roster_view, PkmFullTeam


class Championship(ABC):

    @abstractmethod
    def register(self, c: Competitor):
        pass


class MatchHandlerTree:
    class MatchHandler:

        def __init__(self):
            self.winner: Optional[CompetitorManager] = None
            self.match: Optional[BattleMatch] = None
            self.prev_mh0 = None
            self.prev_mh1 = None

        def run_match(self, debug: bool = False):
            if self.match is None:
                self.match = BattleMatch(self.prev_mh0.winner.competitor, self.prev_mh1.winner.competitor,
                                         self.prev_mh0.winner.team, self.prev_mh1.winner.team, debug=debug)
            if debug:
                print(self.match.competitors[0].name + ' vs ' + self.match.competitors[1].name + '\n')
            if not self.match.finished:
                self.match.run()
                winner = self.match.winner()
                if winner == 0:
                    self.winner = self.match.competitors[0]
                else:
                    self.winner = self.match.competitors[1]
                if debug:
                    print(self.winner.name + ' wins' + '\n')

    def __init__(self, competitors: List[CompetitorManager], enable_debug: bool = False):
        self.competitors = competitors
        self.handlers: List[MatchHandlerTree.MatchHandler] = [MatchHandlerTree.MatchHandler()]
        self.__pos = 0
        self.enable_debug = enable_debug

    def build_tree(self):
        self.__pos = 0
        self.__build_sub_tree(self.competitors)
        self.handlers.reverse()

    def __build_sub_tree(self, cm: List[CompetitorManager]):
        mh = self.handlers[self.__pos]
        self.__pos += 1
        if len(cm) == 1:
            mh.match = BattleMatch(cm[0].competitor, Competitor(), cm[0].team, PkmFullTeam(), debug=self.enable_debug)
            mh.match.finished = True
            mh.winner = cm[0]
        elif len(cm) == 2:
            mh.match = BattleMatch(cm[0].competitor, cm[1].competitor, cm[0].team, cm[1].competitor,
                                   debug=self.enable_debug)
        else:
            half = len(cm) // 2
            mh.prev_mh0 = MatchHandlerTree.MatchHandler()
            mh.prev_mh1 = MatchHandlerTree.MatchHandler()
            self.handlers.append(mh.prev_mh0)
            self.handlers.append(mh.prev_mh1)
            self.__build_sub_tree(cm[:half])
            self.__build_sub_tree(cm[half:])
            mh.match = None

    def run_matches(self, enable_debug: bool = False):
        for handler in self.handlers:
            handler.run_match(enable_debug)


class TreeChampionship(Championship):

    def __init__(self, roster: PkmRoster, meta_data: Optional[MetaData] = None, debug: bool = False):
        self.competitors: List[CompetitorManager] = []
        self.match_tree: Optional[MatchHandlerTree] = None
        self.roster_view = get_pkm_roster_view(roster)
        self.meta_data = meta_data
        self.debug = debug

    def register(self, c: Competitor):
        self.competitors.append(CompetitorManager(c))

    def new_tournament(self):
        random.shuffle(self.competitors)
        self.match_tree = MatchHandlerTree(self.competitors, self.debug)
        self.match_tree.build_tree()

    def run(self):
        for cm in self.competitors:
            cm.team = cm.competitor.team_builder_policy.get_action((self.meta_data, cm.team, self.roster_view,
                                                                    NullTeamValuator.null_team_value))
        self.match_tree.run_matches(self.debug)
