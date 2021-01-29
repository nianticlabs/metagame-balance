from framework.competition.CompetitionObjects import Competitor
from framework.DataObjects import PkmTeam, MetaData
from framework.process.OpponentTeamPrediction import OpponentTeamPrediction
from framework.process.TeamSelection import TeamSelection


class SelectionPhase:

    def __init__(self, c: Competitor, opp_team: PkmTeam):
        self.c = c
        self.opp_team = opp_team
        self.playing_team = None
        self.opp_hyphotesis = None

    @staticmethod
    def extract_oponent_info(opp_team: PkmTeam):
        return None

    def run(self):
        opp = SelectionPhase.extract_oponent_info(self.opp_team)
        oth = OpponentTeamPrediction(self.c.team_hyphotesizer, self.c.meta_data, opp, None)
        self.opp_hyphotesis = oth.get_team_hyphothesis()
        ts = TeamSelection(self.c.selection_policy, self.c.team, self.c.meta_data, self.opp_hyphotesis)
        self.playing_team = ts.get_selected_team()
