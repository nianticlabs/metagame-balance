from typing import List, Any, Tuple
from framework.behaviour import TeamBuilderPolicy
from framework.DataConstants import MAX_TEAM_SIZE, DEFAULT_PKM_N_MOVES
from framework.DataObjects import Pkm, PkmTemplate, PkmRosterView, PkmFullTeam, MetaData, TeamValuation
import random


class RandomTeamBuilderPolicy(TeamBuilderPolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRosterView, PkmFullTeam, MetaData, TeamValuation]) -> PkmFullTeam:
        r_view = d[0]
        pkm_full_team: PkmFullTeam
        pre_selection: List[PkmTemplate] = [r_view.get_pkm_template_view(i).get_copy() for i in
                                            random.sample(range(r_view.n_pkms), MAX_TEAM_SIZE)]
        team: List[Pkm] = []
        for pt in pre_selection:
            team.append(pt.gen_pkm(random.sample(range(len(pt.move_roster)), DEFAULT_PKM_N_MOVES)))
        return PkmFullTeam(team)


class IdleTeamBuilderPolicy(TeamBuilderPolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRosterView, PkmFullTeam, MetaData, TeamValuation]) -> PkmFullTeam:
        return d[1]
