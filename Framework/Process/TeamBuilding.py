from copy import deepcopy
from typing import Any

from Behaviour import TeamBuilderPolicy
from Framework.DataObjects import MetaData, PkmTeam, PkmRoster


class TeamBuilding:

    def __init__(self, tbp: TeamBuilderPolicy, team: PkmTeam, meta_data: MetaData, roster: PkmRoster, val):
        self.tbp = tbp
        self.team = team
        self.meta_data = meta_data
        self.roster = roster
        self.val = val

    def get_team(self) -> Any:
        meta_data = deepcopy(self.meta_data)
        roster = deepcopy(self.roster)
        try:
            team = self.tbp.get_action((meta_data, self.team, roster, self.val))
        except:
            return self.team
        return team
