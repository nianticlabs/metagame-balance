import random
from random import sample
from typing import Tuple, List

from framework.competition.Competitor import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES, DEFAULT_TEAM_SIZE
from framework.datatypes.Objects import PkmFullTeam, get_full_team_view
from framework.engine.PkmBattleEnv import PkmBattleEnv


class BattleMatch:

    def __init__(self, competitor0: Competitor, competitor1: Competitor, full_team0: PkmFullTeam,
                 full_team1: PkmFullTeam, n_battles: int = DEFAULT_MATCH_N_BATTLES, debug: bool = False,
                 render: bool = True):
        self.n_battles: int = n_battles
        self.competitors: Tuple[Competitor, Competitor] = (competitor0, competitor1)
        self.full_teams: Tuple[PkmFullTeam, PkmFullTeam] = (full_team0, full_team1)
        self.wins: List[int] = [0, 0]
        self.debug = debug
        self.render_mode = 'ux' if render else 'console'
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
            try:
                team_ids = list(c0.selector_policy.get_action([team0_view0, team0_view1]))
            except:
                team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
            team0 = full_team0.get_battle_team(team_ids)
            try:
                team_ids = list(c1.selector_policy.get_action([team1_view1, team1_view0]))
            except:
                team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
            team1 = full_team1.get_battle_team(team_ids)
            env = PkmBattleEnv(teams=(team0, team1))
            game += 1
            if self.debug:
                print('GAME ' + str(game) + '\n')
            s = env.reset()
            v = env.game_state_view
            if self.debug:
                env.render(self.render_mode)
            t = False
            while not t:
                o0 = s[0] if a0.requires_encode() else v[0]
                o1 = s[1] if a1.requires_encode() else v[1]
                try:
                    act0 = a0.get_action(o0)
                except:
                    act0 = random.randint(0, 6)
                try:
                    act1 = a1.get_action(o1)
                except:
                    act1 = random.randint(0, 6)
                a = [act0, act1]
                s, _, t, v = env.step(a)
                if self.debug:
                    env.render(self.render_mode)
            self.wins[env.winner] += 1
            if self.wins[env.winner] > self.n_battles // 2:
                break
        if self.debug:
            print('MATCH RESULTS ' + str(self.wins) + '\n')
        a0.close()
        self.finished = True

    def winner(self) -> int:
        """
        Get winner.
        """
        return 0 if self.wins[0] > self.wins[1] else 1
