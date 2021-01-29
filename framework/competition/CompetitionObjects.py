from abc import ABC, abstractmethod
from typing import Tuple, List
from framework.behaviour import BattlePolicy, SelectorPolicy, TeamBuilderPolicy, DataAggregator, TeamPredictor, \
    TeamValuator, BalancePolicy
from framework.behaviour.BalancePolicies import IdleBalancePolicy
from framework.behaviour.BattlePolicies import RandomBattlePolicy
from framework.behaviour.DataAggregators import NullDataAggregator
from framework.behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from framework.behaviour.SelectorPolicies import RandomSelectorPolicy
from framework.behaviour.TeamPredictors import NullTeamPredictor
from framework.behaviour.TeamValuators import NullTeamValuator
from framework.util.PkmRosterGenerators import PkmRosterGenerator
from framework.util.PkmTeamGenerators import TeamSelector
from framework.DataConstants import DEFAULT_MATCH_N_BATTLES
from framework.DataObjects import PkmTeam, PkmFullTeam, MetaData
from framework.process.BattleEngine import PkmBattleEnv
from framework.util.Recording import GamePlayRecorder
import random

random_battle_policy = RandomBattlePolicy()
random_selector_policy = RandomSelectorPolicy()
random_builder_policy = RandomTeamBuilderPolicy()
idle_balance_policy = IdleBalancePolicy()
null_data_aggregator = NullDataAggregator()
null_team_predictor = NullTeamPredictor()
null_team_valuator = NullTeamValuator()


class Competitor(ABC):

    @property
    def battle_policy(self) -> BattlePolicy:
        return random_battle_policy

    @property
    def selector_policy(self) -> SelectorPolicy:
        return random_selector_policy

    @property
    def team_builder_policy(self) -> TeamBuilderPolicy:
        return random_builder_policy

    @property
    def team_prediction_policy(self) -> TeamPredictor:
        return null_team_predictor

    @property
    def data_aggregator_policy(self) -> DataAggregator:
        return null_data_aggregator

    @property
    def team_valuator_policy(self) -> TeamValuator:
        return null_team_valuator

    @property
    def balance_policy(self) -> BalancePolicy:
        return idle_balance_policy

    @property
    @abstractmethod
    def team(self) -> PkmFullTeam:
        pass

    @property
    @abstractmethod
    def meta_info(self) -> MetaData:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def reset(self):
        pass


class Match:

    def __init__(self, competitor0: Competitor, competitor1: Competitor, n_games: int = DEFAULT_MATCH_N_BATTLES,
                 name="match", debug: bool = False, record: bool = False):
        self.n_games: int = n_games
        self.competitors: Tuple[Competitor, Competitor] = (competitor0, competitor1)
        self.debug: bool = debug
        self.name: str = name
        self.wins: List[int] = [0, 0]
        self.record: bool = record

    def run(self):
        c0 = self.competitors[0]
        c1 = self.competitors[1]
        team_selector = TeamSelector(c0.team, c1.team, c0.selector_policy, c1.selector_policy)
        env = PkmBattleEnv(debug=self.debug, teams=[c0.team, c1.team])
        env.set_team_generator(team_selector)
        t = False
        a0 = c0.battle_policy
        a1 = c1.battle_policy
        r = GamePlayRecorder(name=self.name)
        game = 0
        while game < self.n_games:
            game += 1
            if self.debug:
                print('GAME ' + str(game) + '\n')
            s = env.reset()
            v = env.game_state_view
            if self.debug:
                env.render()
            while not t:
                o0 = s[0] if a0.requires_encode() else v[0]
                o1 = s[1] if a1.requires_encode() else v[1]
                a = [a0.get_action(o0), a1.get_action(o1)]
                s, _, t, v = env.step(a)
                if self.record:
                    r.record((s[0], s[1], a[0], a[1], t))
                if self.debug:
                    env.render()
            t = False
            self.wins[env.winner] += 1
            if self.wins[env.winner] > self.n_games // 2:
                break
        if self.debug:
            print('MATCH RESULTS ' + str(self.wins) + '\n')
        if self.record:
            r.save()
        a0.close()

    def records(self) -> List[int]:
        """
        Get match records.

        :return: player 0 winds, player 1 wins
        """
        return self.wins


class Championship(ABC):

    @abstractmethod
    def register_competitor(self, c: Competitor):
        pass


class MatchHandlerTree:
    class MatchHandler:

        def __init__(self):

            self.winner = None
            self.match = None
            self.prev_mh0 = None
            self.prev_mh1 = None

        def run_match(self, enable_debug: bool = False):
            if self.match is None:
                self.match = Match(competitor0=self.prev_mh0.winner, competitor1=self.prev_mh1.winner,
                                   debug=enable_debug)

            if enable_debug:
                print(self.match.competitors[0].name + ' vs ' + self.match.competitors[1].name + '\n')

            self.match.run()
            wins: List[int] = self.match.records()
            if wins[0] > wins[1]:
                self.winner = self.match.competitors[0]
            else:
                self.winner = self.match.competitors[1]

            if enable_debug:
                print(self.winner.name + ' wins' + '\n')

    def __init__(self, competitors: List[Competitor], enable_debug: bool = False):
        self.competitors = competitors
        self.handlers: List[MatchHandlerTree.MatchHandler] = [MatchHandlerTree.MatchHandler()]
        self.__pos = 0
        self.enable_debug = enable_debug

    def build_tree(self):
        self.__pos = 0
        self.__build_sub_tree(self.competitors)
        self.handlers.reverse()

    def __build_sub_tree(self, competitors: List[Competitor]):

        mh = self.handlers[self.__pos]
        self.__pos += 1

        if len(competitors) == 1:
            mh.match = Match(competitor0=competitors[0], competitor1=Competitor(), debug=self.enable_debug)
        elif len(competitors) == 2:
            mh.match = Match(competitor0=competitors[0], competitor1=competitors[1], debug=self.enable_debug)
        else:
            half = len(competitors) // 2
            mh.prev_mh0 = MatchHandlerTree.MatchHandler()
            mh.prev_mh1 = MatchHandlerTree.MatchHandler()
            self.handlers.append(mh.prev_mh0)
            self.handlers.append(mh.prev_mh1)
            self.__build_sub_tree(competitors[:half])
            self.__build_sub_tree(competitors[half:])
            mh.match = None

    def run_matches(self, enable_debug: bool = False):
        for handler in self.handlers:
            handler.run_match(enable_debug)


class TreeChampionship(Championship):

    def __init__(self, pool_generator: PkmRosterGenerator, competitors: List[Competitor] = None,
                 name: str = "Championship", debug: bool = False):
        self.name = name
        self.competitors: List[Competitor] = competitors
        copy_participants = self.competitors.copy()
        random.shuffle(copy_participants)
        self.match_tree = MatchHandlerTree(copy_participants, debug)
        self.match_tree.build_tree()
        self.pool_generator = pool_generator
        self.pool = self.pool_generator.gen_roster()
        self.debug = debug

    def register_competitor(self, c: Competitor):
        self.competitors.append(c)

    def generate_pool(self):
        self.pool = self.pool_generator.gen_roster()

    def create_tournament_tree(self):
        copy_participants = self.competitors.copy()
        random.shuffle(copy_participants)
        self.match_tree = MatchHandlerTree(copy_participants)
        self.match_tree.build_tree()

    def run(self):
        for competitor in self.competitors:
            competitor.team = competitor.team_builder_policy.get_action(self.pool)
        self.match_tree.run_matches(self.debug)
