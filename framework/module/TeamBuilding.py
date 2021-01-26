from framework.competition.CompetitionObjects import Competitor
from framework.DataObjects import MetaData, PkmRoster
from framework.process.TeamBuilding import TeamBuilding
from framework.process.TeamValuation import TeamValuation


class TeamBuildingProcess:

    def __init__(self, c: Competitor, roster: PkmRoster):
        self.c = c
        self.roster = roster
        self.team = None

    def run(self):
        tv = TeamValuation(self.c.team_valuator, self.c.meta_data)
        val = tv.get_team_valuation()
        tb = TeamBuilding(self.c.builder_policy, self.c.team, self.c.meta_data, self.roster, val)
        self.team = tb.get_team()
