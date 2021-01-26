from typing import List
from framework.behaviour import TeamBuilderPolicy
from framework.DataConstants import MAX_TEAM_SIZE, DEFAULT_PKM_N_MOVES
from framework.DataObjects import PkmTeam, Pkm, PkmTemplate, PkmRosterView
import random


class RandomTeamBuilderPolicy(TeamBuilderPolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, r_view: PkmRosterView) -> PkmTeam:
        pre_selection: List[PkmTemplate] = [r_view.get_pkm_template_view(i).get_copy() for i in
                                            random.sample(range(r_view.n_pkms), MAX_TEAM_SIZE)]
        team: List[Pkm] = []
        for pt in pre_selection:
            team.append(pt.gen_pkm(random.sample(range(len(pt.move_roster)), DEFAULT_PKM_N_MOVES)))
        return PkmTeam(team)


class IdleTeamBuilderPolicy(TeamBuilderPolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> PkmTeam:
        return s
