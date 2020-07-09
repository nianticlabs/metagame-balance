import gym

from Engine.PkmBaseStructures import PkmTeam
from Engine.PkmBattleEngine import PkmBattleEngine
from Engine.PkmConstants import DEFAULT_MATCH_N
from Engine.PkmTeamGenerator import RandomGenerator, FixedTeamSelector
from Agent.Abstract.Agent import BattleAgent


class PkmMatchEngine(gym.Env):

    def __init__(self, a0: BattleAgent, a1: BattleAgent, n_games: int = DEFAULT_MATCH_N, debug: bool = False):
        self.team0 = PkmTeam()
        self.team1 = PkmTeam()
        self.rand_generator = RandomGenerator()
        self.team_selector = FixedTeamSelector(self.team0, self.team1)
        self.env = PkmBattleEngine(teams=[self.team0, self.team1])
        self.env.set_team_generator(self.team_selector)
        self.a0 = a0
        self.a1 = a1
        self.n_games = n_games
        self.game = 0
        self.acc_r = [0, 0]
        self.debug = debug
        self.log = ''

    def step(self, action):
        pkm_list0, pkm_list1 = action
        self.team_selector.set_teams(pkm_list0, pkm_list1)
        if self.debug:
            self.log += '\nGame ' + str(self.game) + '\n\nTrainer 0\n' + str(
                self.team_selector.selected_teams[0]) + '\nTrainer 1\n' + str(self.team_selector.selected_teams[1])
        s = self.env.reset()
        v = self.env.trainer_view
        t = False
        # play a game
        while not t:
            o0 = s[0] if self.a0.requires_encode() else v[0]
            o1 = s[1] if self.a1.requires_encode() else v[1]
            a = [self.a0.get_action(o0), self.a1.get_action(o1)]
            s, r, t, v = self.env.step(a)
            self.acc_r[0] += r[0]
            self.acc_r[1] += r[1]
        self.game += 1
        encode0 = self.team_selector.team_views[0][0].encode() + self.team_selector.team_views[0][1].encode()
        encode1 = self.team_selector.team_views[1][0].encode() + self.team_selector.team_views[1][1].encode()
        return [encode0, encode1], self.acc_r, self.game >= self.n_games, self.team_selector.team_views

    def reset(self):
        self.acc_r[0] = 0
        self.acc_r[1] = 0
        self.game = 0
        self.log = ''
        self.team0.set_pkms(self.rand_generator.get_team(0))
        self.team1.set_pkms(self.rand_generator.get_team(1))
        encode0 = self.team_selector.team_views[0][0].encode() + self.team_selector.team_views[0][1].encode()
        encode1 = self.team_selector.team_views[1][0].encode() + self.team_selector.team_views[1][1].encode()
        return [encode0, encode1]

    def render(self, mode='human'):
        print(self.log)
