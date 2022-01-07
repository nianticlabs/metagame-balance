from framework.balance.meta import MetaData
from framework.behaviour import TeamValuator
from framework.datatypes.Objects import PkmFullTeam, TeamValue


class NullTeamValue(TeamValue):

    def compare_to(self, value) -> int:
        return 0


class TeamValuation:
    null_team_value = NullTeamValue()

    def __init__(self, tv: TeamValuator, pkm_full_team: PkmFullTeam, meta_data: MetaData):
        self.tv = tv
        self.pkm_full_team = pkm_full_team
        self.meta_data = meta_data
        # output
        self.value = TeamValuation.null_team_value

    # noinspection PyBroadException
    def run(self):
        try:
            self.value = self.tv.get_action((self.pkm_full_team, self.meta_data))
        except:
            self.value = TeamValuation.null_team_value

    @property
    def team_value(self) -> TeamValue:
        return self.value
