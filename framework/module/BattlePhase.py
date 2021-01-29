from framework.DataConstants import DEFAULT_MATCH_N_BATTLES
from framework.competition.CompetitionObjects import Competitor
from framework.DataObjects import PkmTeam, PkmTeamPrediction, get_full_team_view
from framework.process.BattleEngine import BattleEngine
from framework.process.DataAggregation import DataAggregation
from framework.process.OpponentTeamPrediction import OpponentTeamPrediction
from framework.util.Recording import GamePlayRecorder


class BattlePhase:

    def __init__(self, c0: Competitor, c1: Competitor, team0: PkmTeam, team1: PkmTeam, t0_prediction: PkmTeamPrediction,
                 t1_prediction: PkmTeamPrediction, debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES,
                 rec: GamePlayRecorder = None):
        self.be = BattleEngine(c0.battle_policy, c1.battle_policy, team0, team1, debug, render, n_battles, rec,
                               [t0_prediction, t1_prediction])
        self.otp0 = OpponentTeamPrediction(c0.team_prediction_policy, c0.meta_info,
                                           get_full_team_view(c1.team, partial=True))
        self.otp1 = OpponentTeamPrediction(c1.team_prediction_policy, c1.meta_info,
                                           get_full_team_view(c0.team, partial=True))
        self.da0 = DataAggregation(c0.data_aggregator_policy, c0.meta_info, rec)
        self.da1 = DataAggregation(c1.data_aggregator_policy, c1.meta_info, rec)

    def run(self):
        while not self.be.battle_completed():
            self.be.run_a_turn()
            self.otp0.run()
            self.otp1.run()
        self.da0.run()
        self.da1.run()
