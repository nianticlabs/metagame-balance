from random import sample
from typing import Tuple, List, Optional

from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.behaviour import BattlePolicy
from metagame_balance.vgc.behaviour.TeamPredictors import NullTeamPredictor
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.competition.Competitor import Competitor
from metagame_balance.vgc.datatypes.Constants import DEFAULT_MATCH_N_BATTLES, DEFAULT_TEAM_SIZE
from metagame_balance.vgc.datatypes.Objects import PkmFullTeam, get_full_team_view, PkmTeamPrediction, PkmFullTeamView, PkmTeam
from metagame_balance.vgc.engine.PkmBattleEnv import PkmBattleEnv
from metagame_balance.vgc.util.generator.PkmTeamGenerators import PkmTeamGenerator


def team_selection(c: Competitor, full_team: PkmFullTeam, my_team_view: PkmFullTeamView,
                   opp_team_view: PkmFullTeamView, full_team_size) -> PkmTeam:
    try:
        team_ids = list(c.team_selection_policy.get_action((my_team_view, opp_team_view)))
    except:
        team_ids = sample(range(full_team_size), DEFAULT_TEAM_SIZE)

    return full_team.get_battle_team(team_ids)


class BattleMatch:

    def __init__(self, competitor0: CompetitorManager, competitor1: CompetitorManager,
                 n_battles: int = DEFAULT_MATCH_N_BATTLES, debug: bool = False, render: bool = False,
                 meta_data: Optional[MetaData] = None, random_teams=False, update_meta=False,
                 full_team_size: int = DEFAULT_TEAM_SIZE):
        self.n_battles: int = n_battles
        self.cms: Tuple[CompetitorManager, CompetitorManager] = (competitor0, competitor1)
        self.wins: List[int] = [0, 0]
        self.debug = debug
        self.render_mode = 'ux' if render else 'console'
        self.finished = False
        self.meta_data = meta_data
        self.random_teams = random_teams
        self.update_meta = update_meta
        self.full_team_size = full_team_size

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
        battle = 0
        while battle < self.n_battles:
            team0 = team_selection(c0, full_team0, team0_view0, team0_view1, full_team_size=self.full_team_size)
            team1 = team_selection(c1, full_team1, team1_view1, team1_view0, full_team_size=self.full_team_size)
            battle += 1
            if self.debug:
                print('BATTLE ' + str(battle) + '\n')
            winner = self.__run_battle(a0, a1, team0, team1, team0_prediction, team1_prediction)
            if self.wins[winner] > self.n_battles // 2:
                break
        if self.debug:
            print('MATCH RESULTS ' + str(self.wins) + '\n')
        a0.close()
        full_team0.hide()
        full_team1.hide()
        if self.update_meta:
            self.meta_data.update_with_team(full_team0, self.wins[0] > self.wins[1])
            self.meta_data.update_with_team(full_team1, self.wins[1] > self.wins[0])
        self.finished = True

    def __team_prediction(self, c: Competitor, opp_team_view: PkmFullTeamView) -> PkmTeamPrediction:
        if self.meta_data is None:
            return NullTeamPredictor.null_team_prediction
        else:
            try:
                return c.team_predictor.get_action((opp_team_view, self.meta_data))
            except:
                return NullTeamPredictor.null_team_prediction

    def __run_battle(self, a0: BattlePolicy, a1: BattlePolicy, team0: PkmTeam, team1: PkmTeam,
                     pred0: Optional[PkmTeamPrediction], pred1: Optional[PkmTeamPrediction]) -> int:
        env = PkmBattleEnv((team0, team1), self.debug, [pred1, pred0])
        s = env.reset()
        v = env.game_state_view
        if self.debug:
            env.render(self.render_mode)
        t = False
        while not t:
            o0 = s[0] if a0.requires_encode() else v[0]
            o1 = s[1] if a1.requires_encode() else v[1]
            act0 = a0.get_action(o0)
            act1 = a1.get_action(o1)
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


class RandomTeamsBattleMatch(BattleMatch):

    def __init__(self, gen: PkmTeamGenerator, competitor0: CompetitorManager, competitor1: CompetitorManager,
                 n_battles: int = DEFAULT_MATCH_N_BATTLES, debug: bool = False, render: bool = False,
                 meta_data: Optional[MetaData] = None, random_teams=False, full_team_size: int = DEFAULT_TEAM_SIZE):
        super().__init__(competitor0, competitor1, n_battles, debug, render, meta_data, random_teams,
                         full_team_size=full_team_size)
        self.gen: PkmTeamGenerator = gen

    def run(self):
        a0 = self.cms[0].competitor.battle_policy
        a1 = self.cms[1].competitor.battle_policy
        tie = True
        while tie:
            team0 = self.gen.get_team().get_battle_team([0, 1, 2])
            team1 = self.gen.get_team().get_battle_team([0, 1, 2])
            if self.debug:
                print('BATTLE\n')
            winner0 = self.__run_battle(a0, a1, team0, team1, None, None)
            self.wins[winner0] += 1
            winner1 = self.__run_battle(a0, a1, team1, team0, None, None)
            self.wins[winner1] += 1
            tie = winner0 != winner1
        if self.debug:
            print('MATCH RESULTS ' + str(self.wins) + '\n')
        a0.close()
        self.finished = True
