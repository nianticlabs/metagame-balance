from framework.competition.CompetitionObjects import Competitor
from framework.DataObjects import PkmTeam, MetaData
from framework.process.BattleEngine import BattleEngine
from framework.process.OpponentTeamPrediction import OpponentTeamPrediction


class BattlePhase:

    def __init__(self, c0: Competitor, c1: Competitor, t0: PkmTeam, t1: PkmTeam):
        self.c0 = c0
        self.c1 = c1
        self.t0 = t0
        self.t1 = t1

    def run(self):
        rec = None
        be = BattleEngine(self.c0.battle_policy, self.c1.battle_policy, self.t0, self.t1, rec)

        while not be.match_completed():
            be.run_a_turn()
            oth0 = OpponentTeamPrediction(self.c0.team_hyphotesizer, self.c0.meta_data, opp0, None)
            oth1 = OpponentTeamPrediction(self.c1.team_hyphotesizer, self.c1.meta_data, opp1, None)

            opp_h0 = oth0.get_team_hyphothesis()
            opp_h1 = oth1.get_team_hyphothesis()

        be.terminate()
