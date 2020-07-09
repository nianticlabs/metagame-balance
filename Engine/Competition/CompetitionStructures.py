import random
from abc import ABC, abstractmethod
from typing import Tuple, List, Optional

from Agent.RandomBattleAgent import RandomBattleAgent
from Agent.RandomBuilderAgent import RandomBuilderAgent
from Agent.RandomSelectorAgent import RandomSelectorAgent
from Engine.PkmBaseStructures import PkmTeam
from Engine.PkmBattleEngine import PkmBattleEngine
from Engine.PkmConstants import DEFAULT_MATCH_N
from Engine.PkmPoolGenerator import PkmPoolGenerator
from Engine.PkmTeamGenerator import TeamSelector
from Agent.Abstract.Agent import BattleAgent, SelectorAgent, BuilderAgent
from Util.Recorder import Recorder

random_battle_agent = RandomBattleAgent()
random_selector_agent = RandomSelectorAgent()
random_builder_agent = RandomBuilderAgent()


class Competitor:

    def __init__(self, team: PkmTeam = PkmTeam(), battle_agent: BattleAgent = random_battle_agent,
                 selection_agent: SelectorAgent = random_selector_agent,
                 builder_agent: BuilderAgent = random_builder_agent, name: str = ""):
        self.team: PkmTeam = team
        self.battle_agent: BattleAgent = battle_agent
        self.selection_agent: SelectorAgent = selection_agent
        self.builder_agent: BuilderAgent = builder_agent
        self.name = name

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
        team_selector = TeamSelector(c0.team, c1.team, c0.selection_agent, c1.selection_agent)
        env = PkmBattleEngine(debug=self.debug, teams=[c0.team, c1.team])
        env.set_team_generator(team_selector)
        t = False
        a0 = c0.battle_agent
        a1 = c1.battle_agent
        r = Recorder(name="random_agent")
        game = 0
        while game < self.n_games:
            if self.debug:
                print('GAME ' + str(game) + '\n')
            s = env.reset()
            v = env.trainer_view
            if self.debug:
                env.render()
            game += 1
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

            self.match.run()
            wins: List[int] = self.match.records()
            if wins[0] > wins[1]:
                self.winner = self.match.competitors[0]
            else:
                self.winner = self.match.competitors[1]

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

    def __init__(self, pool_generator: PkmPoolGenerator, competitors: List[Competitor] = None,
                 name: str = "Championship", debug: bool = False):
        self.name = name
        self.competitors: List[Competitor] = competitors
        copy_participants = self.competitors.copy()
        random.shuffle(copy_participants)
        self.match_tree = MatchHandlerTree(copy_participants)
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
            competitor.team = competitor.builder_agent.get_action(self.pool)
        self.match_tree.run_matches(self.debug)
