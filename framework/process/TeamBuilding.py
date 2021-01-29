from copy import deepcopy
from framework.behaviour import TeamBuilderPolicy
from framework.DataObjects import MetaData, PkmFullTeam, PkmRoster, get_pkm_roster_view, TeamValue


class TeamBuilding:

    def __init__(self, tbp: TeamBuilderPolicy, full_team: PkmFullTeam, meta_data: MetaData, roster: PkmRoster,
                 val: TeamValue):
        self.tbp = tbp
        self.full_team = full_team
        self.meta_data = meta_data
        self.roster = roster
        self.val = val

    def get_team(self) -> PkmFullTeam:
        roster = deepcopy(self.roster)
        try:
            team = self.tbp.get_action((self.meta_data, self.full_team, get_pkm_roster_view(roster), self.val))
        except:
            return self.full_team
        return team
