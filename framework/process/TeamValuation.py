
from framework.behaviour import TeamValuator
from framework.DataObjects import MetaData, PkmFullTeam, TeamValue


class TeamValuation:

    null_team_value = TeamValue()

    def __init__(self, tv: TeamValuator, pkm_full_team: PkmFullTeam, meta_data: MetaData):
        self.tv = tv
        self.pkm_full_team = pkm_full_team
        self.meta_data = meta_data

    def get_team_valuation(self) -> TeamValue:
        try:
            val = self.tv.get_action((self.pkm_full_team, self.meta_data))
        except:
            return TeamValuation.null_team_value
        return val
