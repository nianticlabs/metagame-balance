from collections import deque
from FCNN import FCNN
import copy
from vgc.datatypes.Constants import DEFAULT_N_MOVES_PKM, TEAM_SIZE, STATS_OPT_PER_PKM, STATS_OPT_PER_MOVE

class UtilityFunctionManager():
    """
    Responsible for maintaining the utility function
    Specially:
    1) Update the utility function
    2) return/retain two versions for two agents
    3) Perhaps keep pointer to them
    """
    def __init__(self, delay_by: int = 10): #TODO: tune this delay_by
        input_dim = TEAM_SIZE * (STATS_OPT_PER_PKM + DEFAULT_N_MOVES_PKM * STATS_OPT_PER_MOVE) #seems like a wrong place
        init_nn = FCNN([input_dim, 128, 64, 1])
        init_nn.compile() #consider using SGD over Adam
        self.list_U_fn = deque([init_nn], delay_by) # Neural network!!

    def agent_U_function(self):

        return self.list_U_fn[-1] # or a predict function

    def adversary_U_function(self):

        return self.list_U_fn[0]
