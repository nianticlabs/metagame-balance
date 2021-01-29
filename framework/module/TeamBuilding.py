from framework.competition.CompetitionObjects import Competitor
from framework.DataObjects import PkmRoster, PkmFullTeam
from framework.process.TeamBuilding import TeamBuilding
from framework.process.TeamValuation import TeamValuation


class TeamBuildingProcess:

    def __init__(self, c: Competitor, roster: PkmRoster):
        self.tv = TeamValuation(c.team_valuator_policy, c.team, c.meta_info)
        # TODO self.tv.team_value
        self.tb = TeamBuilding(c.team_builder_policy, c.team, c.meta_info, roster, self.tv.team_value)

    def run(self):
        self.tv.run()
        self.tb.run()

    def output(self) -> PkmFullTeam:
        return self.tb.team
