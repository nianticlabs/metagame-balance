from Framework.Competition.CompetitionStructures import Competitor
from Framework.DataObjects import PkmTeam, MetaData
from Framework.Process.BattleEngine import BattleEngine
from Framework.Process.OpponentTeamHyphotesizing import OponentTeamHyphotesizing


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
            be.run_step()
            oth0 = OponentTeamHyphotesizing(self.c0.team_hyphotesizer, self.c0.meta_data, opp0, None)
            oth1 = OponentTeamHyphotesizing(self.c1.team_hyphotesizer, self.c1.meta_data, opp1, None)

            opp_h0 = oth0.get_team_hyphothesis()
            opp_h1 = oth1.get_team_hyphothesis()

        be.terminate()
