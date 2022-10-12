from typing import List, Tuple, Optional

from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.behaviour import TeamBuildPolicy
from metagame_balance.vgc.datatypes.Constants import DEFAULT_TEAM_SIZE
from metagame_balance.vgc.datatypes.Objects import Pkm, PkmRoster, PkmFullTeam


class RandomTeamBuildPolicy(TeamBuildPolicy):

    def close(self):
        pass

    def get_action(self, d: Tuple[MetaData, Optional[PkmFullTeam], PkmRoster]) -> PkmFullTeam:
        roster = d[2]
        """
        Removed views (access the roster's directly!)
        """
        import random
        pre_selection = random.sample(list(roster), DEFAULT_TEAM_SIZE)
        team: List[Pkm] = []
        for pt in pre_selection:
            team.append(pt.gen_pkm())
        return PkmFullTeam(team)
