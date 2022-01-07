from datetime import datetime

from framework.competition.Competition import Competitor
from framework.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from framework.datatypes.Objects import PkmTeam, PkmTeamPrediction, get_full_team_view, PkmFullTeam
from framework.process.BattleEngine import BattleEngine
from framework.process.DataAggregation import DataAggregation
from framework.process.OpponentTeamPrediction import OpponentTeamPrediction
from framework.util.Recording import MetaGameSubscriber, DataDistributionManager, GamePlayRecorder


class BattlePhase:

    def __init__(self, c0: Competitor, c1: Competitor, team0: PkmTeam, full_team0: PkmFullTeam, team1: PkmTeam,
                 full_team1: PkmFullTeam, t0_prediction: PkmTeamPrediction, t1_prediction: PkmTeamPrediction,
                 mgs0: MetaGameSubscriber, mgs1: MetaGameSubscriber, ddm: DataDistributionManager = None, debug=False,
                 render=True, n_battles=DEFAULT_MATCH_N_BATTLES):
        self.c0 = c0
        self.c1 = c1
        self.team0 = team0
        self.team1 = team1
        self.be = BattleEngine(c0.battle_policy, c1.battle_policy, team0, team1, debug, render, n_battles,
                               [t0_prediction, t1_prediction])
        self.otp0 = OpponentTeamPrediction(c0.team_prediction_policy, c0.meta_data,
                                           get_full_team_view(full_team1, partial=True))
        self.otp1 = OpponentTeamPrediction(c1.team_prediction_policy, c1.meta_data,
                                           get_full_team_view(full_team0, partial=True))
        self.da0 = DataAggregation(c0.data_aggregator_policy, c0.meta_data, mgs0)
        self.da1 = DataAggregation(c1.data_aggregator_policy, c1.meta_data, mgs1)
        self.ddm = ddm

    def run(self):
        rec = GamePlayRecorder(c0=self.c0.name, c1=self.c1.name, t0=self.team0.get_pkm_list(),
                               t1=self.team1.get_pkm_list())
        rec.init(name=datetime.now().strftime("%Y%m%d-%H%M%S.%f") + "_" + self.c0.name + "_" + self.c1.name)
        completed = False
        while not completed:
            self.be.run_a_turn(rec)
            self.otp0.run()
            self.otp1.run()
            completed = self.be.battle_completed()
        rec.save()
        self.ddm.signal_concluded_battle(rec.name)
        self.da0.run()
        self.da1.run()

    @property
    def winner(self) -> int:
        return self.be.winner
