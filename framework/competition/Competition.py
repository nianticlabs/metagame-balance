import random
from abc import ABC, abstractmethod
from typing import Tuple, List, Optional

from framework.behaviour.TeamValuators import NullTeamValuator
from framework.competition import CompetitorManager
from framework.competition.Competitor import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from framework.datatypes.Objects import get_full_team_view, PkmRoster, get_pkm_roster_view, PkmFullTeam
from framework.process.BattleEngine import PkmBattleEnv


class Match:

    def __init__(self, competitor0: Competitor, competitor1: Competitor, full_team0: PkmFullTeam,
                 full_team1: PkmFullTeam, n_battles: int = DEFAULT_MATCH_N_BATTLES, debug: bool = False):
        self.n_battles: int = n_battles
        self.competitors: Tuple[Competitor, Competitor] = (competitor0, competitor1)
        self.full_teams: Tuple[PkmFullTeam, PkmFullTeam] = (full_team0, full_team1)
        self.wins: List[int] = [0, 0]
        self.debug: bool = debug
        self.finished = False

    def run(self):
        c0 = self.competitors[0]
        c1 = self.competitors[1]
        full_team0 = self.full_teams[0]
        full_team1 = self.full_teams[1]
        team0_view0 = get_full_team_view(full_team0)
        team0_view1 = get_full_team_view(full_team1, partial=True)
        team1_view1 = get_full_team_view(full_team1)
        team1_view0 = get_full_team_view(full_team0, partial=True)
        a0 = c0.battle_policy
        a1 = c1.battle_policy
        game = 0
        while game < self.n_battles:
            team0 = full_team0.get_battle_team(list(c0.selector_policy.get_action([team0_view0, team0_view1])))
            team1 = full_team1.get_battle_team(list(c1.selector_policy.get_action([team1_view1, team1_view0])))
            env = PkmBattleEnv(debug=self.debug, teams=(team0, team1))
            game += 1
            if self.debug:
                print('GAME ' + str(game) + '\n')
            s = env.reset()
            v = env.game_state_view
            if self.debug:
                env.render()
            t = False
            while not t:
                o0 = s[0] if a0.requires_encode() else v[0]
                o1 = s[1] if a1.requires_encode() else v[1]
                a = [a0.get_action(o0), a1.get_action(o1)]
                s, _, t, v = env.step(a)
                if self.debug:
                    env.render()
            self.wins[env.winner] += 1
            if self.wins[env.winner] > self.n_battles // 2:
                break
        if self.debug:
            print('MATCH RESULTS ' + str(self.wins) + '\n')
        a0.close()
        self.finished = True

    def records(self) -> List[int]:
        """
        Get match records.

        :return: player 0 winds, player 1 wins
        """
        return self.wins


class Championship(ABC):

    @abstractmethod
    def register(self, c: Competitor):
        pass


class MatchHandlerTree:
    class MatchHandler:

        def __init__(self):
            self.winner: Optional[CompetitorManager] = None
            self.match: Optional[Match] = None
            self.prev_mh0 = None
            self.prev_mh1 = None

        def run_match(self, debug: bool = False):
            if self.match is None:
                self.match = Match(self.prev_mh0.winner.competitor, self.prev_mh1.winner.competitor,
                                   self.prev_mh0.winner.team, self.prev_mh1.winner.team, debug=debug)
            if debug:
                print(self.match.competitors[0].name + ' vs ' + self.match.competitors[1].name + '\n')
            if not self.match.finished:
                self.match.run()
                wins: List[int] = self.match.records()
                if wins[0] > wins[1]:
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
            mh.match = Match(cm[0].competitor, Competitor(), cm[0].team, PkmFullTeam(), debug=self.enable_debug)
            mh.match.finished = True
            mh.winner = cm[0]
        elif len(cm) == 2:
            mh.match = Match(cm[0].competitor, cm[1].competitor, cm[0].team, cm[1].competitor, debug=self.enable_debug)
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

    def __init__(self, roster: PkmRoster, debug: bool = False):
        self.competitors: List[CompetitorManager] = []
        self.match_tree: Optional[MatchHandlerTree] = None
        self.roster_view = get_pkm_roster_view(roster)
        self.debug = debug

    def register(self, c: Competitor):
        self.competitors.append(CompetitorManager(c))

    def new_tournament(self):
        random.shuffle(self.competitors)
        self.match_tree = MatchHandlerTree(self.competitors, self.debug)
        self.match_tree.build_tree()

    def run(self):
        for cm in self.competitors:
            cm.team = cm.competitor.team_builder_policy.get_action((cm.meta_data, cm.team, self.roster_view,
                                                                    NullTeamValuator.null_team_value))
        self.match_tree.run_matches(self.debug)
