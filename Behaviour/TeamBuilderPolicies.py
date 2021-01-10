from typing import List
from Behaviour import TeamBuilderPolicy
from Framework.DataConstants import MAX_TEAM_SIZE, N_MOVES
from Framework.DataObjects import PkmTeam, PkmRoster, Pkm, PkmTemplate
import random


class RandomTeamBuilderPolicy(TeamBuilderPolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> PkmTeam:
        p: PkmRoster = s
        pre_selection: List[PkmTemplate] = random.sample(p, MAX_TEAM_SIZE)
        team: List[Pkm] = []
        for pt in pre_selection:
            team.append(pt.get_pkm(random.sample(range(len(pt.move_roster)), N_MOVES)))
        return PkmTeam(team)
