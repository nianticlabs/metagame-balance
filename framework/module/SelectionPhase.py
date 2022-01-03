from typing import Tuple

from framework.competition.CompetitionObjects import Competitor
from framework.datatypes.Objects import PkmFullTeam, get_full_team_view, PkmTeam, PkmTeamPrediction
from framework.process.OpponentTeamPrediction import OpponentTeamPrediction
from framework.process.TeamSelection import TeamSelection


class SelectionPhase:

    def __init__(self, c: Competitor, opp_full_team: PkmFullTeam):
        self.opp_full_team = opp_full_team
        self.otp = OpponentTeamPrediction(c.team_prediction_policy, c.meta_data,
                                          get_full_team_view(opp_full_team, partial=True))
        self.ts = TeamSelection(c.selector_policy, c.team, opp_full_team)

    def run(self):
        self.opp_full_team.reveal()
        self.otp.run()
        self.ts.run(self.otp.team_prediction)
        self.opp_full_team.hide_pkms()

    def output(self) -> Tuple[PkmTeam, PkmTeamPrediction]:
        return self.ts.selected_team, self.otp.team_prediction
