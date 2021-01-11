from Framework.Competition.CompetitionStructures import Competitor
from Framework.DataObjects import MetaData, PkmRoster
from Framework.Process.TeamBuilding import TeamBuilding
from Framework.Process.TeamValuation import TeamValuation


class TeamBuildingProcess:

    def __init__(self, c: Competitor, meta_data: MetaData, roster: PkmRoster):
        self.c = c
        self.meta_data = meta_data
        self.roster = roster
        self.team = None

    def run(self):
        tv = TeamValuation(self.c.team_valuator, self.meta_data)
        val = tv.get_team_valuation()
        tb = TeamBuilding(self.c.builder_policy, self.c.team, self.meta_data, self.roster, val)
        self.team = tb.get_team()
