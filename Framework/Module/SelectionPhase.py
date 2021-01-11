from Framework.Competition.CompetitionStructures import Competitor
from Framework.DataObjects import PkmTeam, MetaData
from Framework.Process.OpponentTeamHyphotesizing import OponentTeamHyphotesizing
from Framework.Process.TeamSelection import TeamSelection


class SelectionPhase:

    def __init__(self, c: Competitor, opp_team: PkmTeam, meta_data: MetaData):
        self.c = c
        self.opp_team = opp_team
        self.meta_data = meta_data
        self.playing_team = None
        self.opp_hyphotesis = None

    @staticmethod
    def extract_oponent_info(opp_team: PkmTeam):
        return None

    def run(self):
        opp = SelectionPhase.extract_oponent_info(self.opp_team)
        oth = OponentTeamHyphotesizing(self.c.team_hyphotesizer, self.meta_data, opp, None)
        self.opp_hyphotesis = oth.get_team_hyphothesis()
        ts = TeamSelection(self.c.selection_policy, self.c.team, self.meta_data, self.opp_hyphotesis)
        self.playing_team = ts.get_selected_team()
