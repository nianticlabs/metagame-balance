import random
from typing import List

from Behaviour.Abstract.Behaviour import TeamBuilderPolicy
from Engine.DataObjects import PkmTeam, Pkm, PkmTemplate
from Engine.DataConstants import N_MOVES, MAX_TEAM_SIZE
from Engine.Competition.PkmRosterGenerator import PkmRoster


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
