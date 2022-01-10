import random
from abc import ABC, abstractmethod
from typing import List, Optional

from framework.balance.meta import MetaData
from framework.behaviour.TeamValuators import NullTeamValuator
from framework.competition import CompetitorManager
from framework.competition.BattleMatch import BattleMatch
from framework.competition.Competitor import Competitor
from framework.datatypes.Objects import PkmRoster, get_pkm_roster_view


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
                self.match = BattleMatch(self.prev_mh0.winner, self.prev_mh1.winner, debug=debug)
            if debug:
                print(self.match.cms[0].competitor.name + ' vs ' + self.match.cms[1].competitor.name + '\n')
            if not self.match.finished:
                self.match.run()
                winner = self.match.winner()
                if winner == 0:
                    self.winner = self.match.cms[0]
                else:
                    self.winner = self.match.cms[1]
                if debug:
                    print(self.winner.competitor.name + ' wins' + '\n')

    def __init__(self, competitors: List[CompetitorManager], debug: bool = False,
                 meta_data: Optional[MetaData] = None):
        self.meta_data = meta_data
        self.competitors = competitors
        self.handlers: List[MatchHandlerTree.MatchHandler] = [MatchHandlerTree.MatchHandler()]
        self.pos = 0
        self.debug = debug

    def build_tree(self):
        self.__build_sub_tree(self.competitors)
        self.handlers.reverse()

    def __build_sub_tree(self, cm: List[CompetitorManager]):
        mh = self.handlers[self.pos]
        self.pos += 1
        if len(cm) == 1:
            mh.match = BattleMatch(cm[0], CompetitorManager(Competitor()), debug=self.debug, meta_data=self.meta_data)
            mh.match.finished = True
            mh.winner = cm[0]
        elif len(cm) == 2:
            mh.match = BattleMatch(cm[0], cm[1], debug=self.debug)
        else:
            half = len(cm) // 2
            mh.prev_mh0 = MatchHandlerTree.MatchHandler()
            mh.prev_mh1 = MatchHandlerTree.MatchHandler()
            self.handlers.append(mh.prev_mh0)
            self.handlers.append(mh.prev_mh1)
            self.__build_sub_tree(cm[:half])
            self.__build_sub_tree(cm[half:])

    def run_matches(self, debug: bool = False):
        for handler in self.handlers:
            handler.run_match(debug)


class TreeChampionship(Championship):

    def __init__(self, roster: PkmRoster, meta_data: Optional[MetaData] = None, debug: bool = False):
        self.competitors: List[CompetitorManager] = []
        self.match_tree: Optional[MatchHandlerTree] = None
        self.roster_view = get_pkm_roster_view(roster)
        self.meta_data = meta_data
        self.debug = debug

    def register(self, c: Competitor):
        cm = CompetitorManager(c)
        cm.team = cm.competitor.team_build_policy.get_action((self.meta_data, cm.team, self.roster_view,
                                                              NullTeamValuator.null_team_value))
        self.competitors.append(cm)

    def new_tournament(self):
        random.shuffle(self.competitors)
        self.match_tree = MatchHandlerTree(self.competitors, self.debug)
        self.match_tree.build_tree()

    def run(self):
        self.match_tree.run_matches(self.debug)
