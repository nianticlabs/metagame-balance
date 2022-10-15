from metagame_balance.vgc.datatypes.Constants import DEFAULT_TEAM_SIZE
from metagame_balance.vgc.datatypes.Objects import PkmFullTeam, PkmRoster, Pkm
from metagame_balance.vgc.balance.meta import MetaData
from typing import List, Tuple, Optional
from metagame_balance.vgc.behaviour import TeamBuildPolicy


class FixedTeamPolicy(TeamBuildPolicy):
    def __init__(self, team_size=DEFAULT_TEAM_SIZE):
        self.team_size = team_size
        self.team_idx = []

    def set_team(self, team_idxs):
        self.team_idx = team_idxs

    def get_action(self, d: Tuple[MetaData, Optional[PkmFullTeam], PkmRoster]) -> PkmFullTeam:

        team: List[Pkm] = []
        roster = list(d[2])
        for i in range(self.team_size):
            team.append(roster[self.team_idx[i]].gen_pkm())

        return PkmFullTeam(team)

    def close(self):
        return
