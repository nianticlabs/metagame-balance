from collections import deque
<<<<<<< HEAD
from FCNN import FCNN
=======
>>>>>>> defc635 (merge issue 1)

class UtilityFunctionManager():
    """
    Responsible for maintaining the utility function
    Specially:
    1) Update the utility function
    2) return/retain two versions for two agents
    3) Perhaps keep pointer to them
    """
    def __init__(self, delay_by: int = 10): #TODO: turn this delay_by
        self.list_U_fn = deque([FCNN([100,231,1])], delay_by) # Neural network!!

    def update(self, team, reward) -> None:

        raise NotImplementedError

    def agent_U_function(self):

        return self.list_U_fn[-1] # or a predict function

    def adversary_U_function(self):

        return self.list_U_fn[0]
