from collections import deque
from metagame_balance.FCNN import FCNN
from metagame_balance.vgc.datatypes.Constants import STAGE_2_STATE_DIM

class UtilityFunctionManager():
    """
    Responsible for maintaining the utility function
    Specially:
    1) Update the utility function
    2) return/retain two versions for two agents
    3) Perhaps keep pointer to them
    """
    def __init__(self, delay_by: int = 10): #TODO: tune this delay_by
        input_dim = STAGE_2_STATE_DIM
        init_nn = FCNN([input_dim, 128, 64, 1])
        init_nn.compile() #consider using SGD over Adam
        self.list_u_fn = deque([init_nn], delay_by) # Neural network!!

    def add(self, u: FCNN):
        self.list_u_fn.append(u)

    def agent_U_function(self):

        return self.list_u_fn[-1] # or a predict function

    def adversary_U_function(self):

        return self.list_u_fn[0]
