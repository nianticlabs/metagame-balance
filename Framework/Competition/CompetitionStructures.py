from abc import ABC, abstractmethod
from typing import Tuple, List
from Behaviour import BattlePolicy, SelectorPolicy, TeamBuilderPolicy, DataAggregator, TeamHyphotesizer, TeamValuator, \
    BalancePolicy
from Behaviour.BalancePolicies import IdleBalancePolicy
from Behaviour.BattlePolicies import RandomBattlePolicy
from Behaviour.DataAggregators import NullDataAggregator
from Behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from Behaviour.SelectorPolicies import RandomSelectorPolicy
from Behaviour.TeamHyphotesizers import NullTeamHyphotesizer
from Behaviour.TeamValuators import NullTeamValuator
from Util.PkmRosterGenerators import PkmRosterGenerator
from Util.PkmTeamGenerators import TeamSelector
from Framework.DataConstants import DEFAULT_MATCH_N
from Framework.DataObjects import PkmTeam, MetaData
from Framework.Process.BattleEngine import PkmBattleEnv
from Util.Recorders import FileRecorder
import random

random_battle_agent = RandomBattlePolicy()
random_selector_agent = RandomSelectorPolicy()
random_builder_agent = RandomTeamBuilderPolicy()
idle_balance_policy = IdleBalancePolicy()
null_data_aggregator = NullDataAggregator()
null_team_hyphotesizer = NullTeamHyphotesizer()
null_team_valuator = NullTeamValuator()
null_meta_data = MetaData()


class Competitor:

    def __init__(self, team: PkmTeam = PkmTeam(), battle_agent: BattlePolicy = random_battle_agent,
                 selection_agent: SelectorPolicy = random_selector_agent,
                 builder_agent: TeamBuilderPolicy = random_builder_agent,
                 balance_policy: BalancePolicy = idle_balance_policy,
                 data_aggregator: DataAggregator = null_data_aggregator,
                 team_hyphotesizer: TeamHyphotesizer = null_team_hyphotesizer,
                 team_valuator: TeamValuator = null_team_valuator,
                 meta_data: MetaData = null_meta_data,
                 name: str = ""):
        self.team: PkmTeam = team
        self.battle_policy: BattlePolicy = battle_agent
        self.selection_policy: SelectorPolicy = selection_agent
        self.builder_policy: TeamBuilderPolicy = builder_agent
        self.balance_policy: BalancePolicy = balance_policy
        self.data_aggregator: DataAggregator = data_aggregator
        self.team_hyphotesizer: TeamHyphotesizer = team_hyphotesizer
        self.team_valuator: TeamValuator = team_valuator
        self.name = name
        self.meta_data = meta_data

    def __str__(self):
        return str(self.team)

    def reset(self):
        self.team.reset()


class Match:

    def __init__(self, competitor0: Competitor, competitor1: Competitor, n_games: int = DEFAULT_MATCH_N, name="match",
                 debug: bool = False, record: bool = False):
        self.n_games: int = n_games
        self.competitors: Tuple[Competitor, Competitor] = (competitor0, competitor1)
        self.debug: bool = debug
        self.name: str = name
        self.wins: List[int] = [0, 0]
        self.record: bool = record

    def run(self):
        c0 = self.competitors[0]
        c1 = self.competitors[1]
        team_selector = TeamSelector(c0.team, c1.team, c0.selection_policy, c1.selection_policy)
        env = PkmBattleEnv(debug=self.debug, teams=[c0.team, c1.team])
        env.set_team_generator(team_selector)
        t = False
        a0 = c0.battle_policy
        a1 = c1.battle_policy
        r = FileRecorder(name="random_agent")
        game = 0
        while game < self.n_games:
            game += 1
            if self.debug:
                print('GAME ' + str(game) + '\n')
            s = env.reset()
            v = env.trainer_view
            if self.debug:
                env.render()
            while not t:
                o0 = s[0] if a0.requires_encode() else v[0]
                o1 = s[1] if a1.requires_encode() else v[1]
                a = [a0.get_action(o0), a1.get_action(o1)]
                if self.record:
                    r.record((s[0], a[0], game))
                s, _, t, v = env.step(a)
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
        self.pool = self.pool_generator.get_pool()
        self.debug = debug

    def register_competitor(self, c: Competitor):
        self.competitors.append(c)

    def generate_pool(self):
        self.pool = self.pool_generator.get_pool()

    def create_tournament_tree(self):
        copy_participants = self.competitors.copy()
        random.shuffle(copy_participants)
        self.match_tree = MatchHandlerTree(copy_participants)
        self.match_tree.build_tree()

    def run(self):
        for competitor in self.competitors:
            competitor.team = competitor.builder_policy.get_action(self.pool)
        self.match_tree.run_matches(self.debug)
