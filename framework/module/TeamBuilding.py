from framework.competition.Competition import Competitor
from framework.datatypes.Objects import PkmRoster, PkmFullTeam
from framework.process.TeamBuilding import TeamBuilding
from framework.process.TeamValuation import TeamValuation


class TeamBuildingProcess:

    def __init__(self, c: Competitor, team: PkmFullTeam, roster: PkmRoster):
        self.tv = TeamValuation(c.team_valuator_policy, team, c.meta_data)
        self.tb = TeamBuilding(c.team_builder_policy, team, c.meta_data, roster)

    def run(self):
        self.tv.run()
        self.tb.run(self.tv.team_value)

    def output(self) -> PkmFullTeam:
        return self.tb.team
