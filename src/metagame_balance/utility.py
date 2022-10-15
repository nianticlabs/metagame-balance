from collections import deque
from copy import deepcopy

from torch import nn

class UtilityFunctionManager:
    """
    Responsible for maintaining the utility function
    Specially:
    1) Update the utility function
    2) return/retain two versions for two agents
    3) Perhaps keep pointer to them
    """

    def __init__(self, u, delay_by: int = 10):  # TODO: tune this delay_by
        self.list_u_fn = deque([u], delay_by)
        self.list_u_fn.append(deepcopy(u))

    def add(self, u):
        raise Exception("shouldn't add")
        self.list_u_fn.append(u)

    def agent_U_function(self):
        return self.list_u_fn[-1]  # or a predict function

    def adversary_U_function(self) -> nn.Module:
        return self.list_u_fn[0]

    def __getitem__(self, item):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

