from vgc.behaviour import TeamBuildPolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_TEAM_SIZE
from typing import List, Tuple, Optional

from vgc.balance.meta import MetaData
from vgc.datatypes.Objects import PkmFullTeam, PkmRoster
class SeqSoftmaxSelectionPolicy(TeamBuildPolicy):

    def __init__(self, utility_function, update_policy: bool):

        self.u = utility_function ### This should be function pointer
        self._updatable = update_policy

    def get_action(self, d: Tuple[MetaData, Optional[PkmFullTeam], PkmRoster]) -> PkmFullTeam:

        team: List[Pkm] = []
        roster = list(d[2])
        for i in range(DEFAULT_TEAM_SIZE):
            #create vector
            import random
            selection_idx = int(random.random() * len(roster))
            team.append(roster[selection_idx].gen_pkm())

        #update if you are the primary agent else discard
        return PkmFullTeam(team)

    def update(self, reward: float) -> None:

        if self._updatable is False:
            return

    def close(self) -> None:
        """
        considering dumping the recent neural network to a file here
        """
        return
