from vgc.behaviour import TeamBuildPolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_TEAM_SIZE

class SeqSoftmaxSelectionPolicy(TeamBuildPolicy):

    def __init__(self, utility_function):

        self.u = utility_function ### This should be function pointer

    def get_action(self, d: Tuple[MetaData, Optional[PkmFullTeam], PkmRoster]) -> PkmFullTeam:

        team: List[Pkm]
        for i in range(DEFAULT_TEAM_SIZE):
            #create vector
            selection_idx = sample_from_softmax
            team.append(d[2][selection_idx].gen_pkm())

        #update if you are the primary agent else discard
        return PkmFullTeam(team)

