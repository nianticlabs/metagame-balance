import random
from typing import List, Tuple, Optional

from vgc.balance.meta import MetaData
from vgc.behaviour import TeamBuildPolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_TEAM_SIZE
from vgc.datatypes.Objects import Pkm, PkmTemplate, PkmRoster, PkmFullTeam, PkmTemplateView, PkmMove, MoveView, PkmRosterView


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
