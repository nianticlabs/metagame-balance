import numpy as np
from scipy.special import softmax

from metagame_balance.rpsfw.Rosters import RPSFWRoster
from metagame_balance.rpsfw.util.Constants import RPSFWItems
from metagame_balance.utility import UtilityFunctionManager


class SoftmaxCompetitor:
    def __init__(self, name:str, utility_fn: UtilityFunctionManager,
                get_u_fn, update_policy:bool, lr: float = 1e-2):
        self.name = name
        self.utility_fn = utility_fn

        self.get_u_fn = get_u_fn
        self.lr = lr
        self.greedy = False
        self._updatable = update_policy

    def set_greedy(self, greedy: bool):
        self.greedy = greedy

    def get_action(self, roster: RPSFWRoster):
        u = self.get_u_fn()
        values = u.get_all_vals()
        if self.greedy:
            selection_idx = np.argmax(values)
        else:
            selection_idx = np.random.choice(range(len(roster)), p=softmax(values))

        return selection_idx

    def update(self, selection: RPSFWItems, reward: float):
        if self._updatable is False:
            reward = -reward
            #let this mean advs
            #return
        u = self.get_u_fn()
        #from scipy.special import softmax
        #print(self.name, reward, selection, list(softmax(u.get_all_vals())))
        u[selection] = (1 - self.lr) * u[selection] + self.lr * reward
