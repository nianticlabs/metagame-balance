import random
from random import sample
from typing import Tuple, List, Optional

from framework.balance.meta import MetaData
from framework.behaviour import BattlePolicy
from framework.behaviour.TeamPredictors import NullTeamPredictor
from framework.competition import CompetitorManager
from framework.competition.Competitor import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES, DEFAULT_TEAM_SIZE
from framework.datatypes.Objects import PkmFullTeam, get_full_team_view, PkmTeamPrediction, PkmFullTeamView, PkmTeam
from framework.engine.PkmBattleEnv import PkmBattleEnv


def team_selection(c: Competitor, full_team: PkmFullTeam, my_team_view: PkmFullTeamView,
                   opp_team_view: PkmFullTeamView) -> PkmTeam:
    try:
        team_ids = list(c.team_selection_policy.get_action((my_team_view, opp_team_view)))
    except:
        team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
    return full_team.get_battle_team(team_ids)


class BattleMatch:

    def __init__(self, competitor0: CompetitorManager, competitor1: CompetitorManager,
                 n_battles: int = DEFAULT_MATCH_N_BATTLES, debug: bool = False, render: bool = False,
                 meta_data: Optional[MetaData] = None):
        self.n_battles: int = n_battles
        self.cms: Tuple[CompetitorManager, CompetitorManager] = (competitor0, competitor1)
        self.wins: List[int] = [0, 0]
        self.debug = debug
        self.render_mode = 'ux' if render else 'console'
        self.finished = False
        self.meta_data = meta_data

    def run(self):
        c0 = self.cms[0].competitor
        c1 = self.cms[1].competitor
        full_team0 = self.cms[0].team
        full_team1 = self.cms[1].team
        full_team0.reveal()
        full_team1.reveal()
        team0_view0 = get_full_team_view(full_team0)
        team1_view1 = get_full_team_view(full_team1)
        team1_prediction = self.__team_prediction(c0, team1_view1)
        team0_prediction = self.__team_prediction(c1, team0_view0)
        team0_view1 = get_full_team_view(full_team1, team1_prediction, partial=True)
        team1_view0 = get_full_team_view(full_team0, team0_prediction, partial=True)
        a0 = c0.battle_policy
        a1 = c1.battle_policy
        game = 0
        while game < self.n_battles:
            team0 = team_selection(c0, full_team0, team0_view0, team0_view1)
            team1 = team_selection(c1, full_team1, team1_view1, team1_view0)
            game += 1
            if self.debug:
                print('GAME ' + str(game) + '\n')
            winner = self.__run_battle(a0, a1, team0, team1)
            if self.wins[winner] > self.n_battles // 2:
                break
        if self.debug:
            print('MATCH RESULTS ' + str(self.wins) + '\n')
        a0.close()
        full_team0.hide()
        full_team1.hide()
        self.finished = True

    def __team_prediction(self, c: Competitor, opp_team_view: PkmFullTeamView) -> PkmTeamPrediction:
        if self.meta_data is None:
            return NullTeamPredictor.null_team_prediction
        else:
            try:
                return c.team_predictor.get_action((opp_team_view, self.meta_data))
            except:
                return NullTeamPredictor.null_team_prediction

    def __run_battle(self, a0: BattlePolicy, a1: BattlePolicy, team0: PkmTeam, team1: PkmTeam) -> int:
        env = PkmBattleEnv(teams=(team0, team1), debug=self.debug)
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
        return env.winner

    def winner(self) -> int:
        """
        Get winner.
        """
        return 0 if self.wins[0] > self.wins[1] else 1
