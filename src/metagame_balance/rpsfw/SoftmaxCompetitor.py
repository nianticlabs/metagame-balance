import numpy as np
from scipy.special import softmax

from metagame_balance.utility import UtilityFunctionManager


class SoftmaxCompetitor:
    def __init__(self, name:str,
                utility_fn, update_policy:bool, lr: float = 1e-1):
        self.name = name

        self.utility_fn = utility_fn
        self.lr = lr
        self.greedy = False
        self._updatable = update_policy

    def set_greedy(self, greedy: bool):
        self.greedy = greedy

    def get_action(self, roster):
        u = self.utility_fn
        values = u.get_all_vals()
        if self.greedy:
            selection_idx = np.argmax(values)
        else:
            selection_idx = np.random.choice(range(len(roster)), p=softmax(values))

        return selection_idx

    def get_u_fn(self):
        return self.utility_fn

    def _get_agent_reward(self, raw_reward:float) -> float:
        if self.name == "agent":
            return raw_reward
        elif self.name == "adversary":
            return -raw_reward
        else:
            raise Exception("Unknown Player Name")

    def update(self, selection, raw_reward: float):
        u = self.utility_fn
        reward = self._get_agent_reward(raw_reward)
        #from scipy.special import softmax
        #print(self.name, reward, selection, list(softmax(u.get_all_vals())))
        u[selection] = (1 - self.lr) * u[selection] + self.lr * reward
