import numpy as np
from scipy.special import softmax

from metagame_balance.rpsfw.Rosters import RPSFWRoster
from metagame_balance.rpsfw.util.Constants import RPSFWItems
from metagame_balance.utility import UtilityFunctionManager


class SoftmaxUtilityFunction:
    def __init__(self, size: int):
        # optimistic initialization maybe
        self.values = np.ones(size)

    def __getitem__(self, key: RPSFWItems) -> float:
        return self.values[key]

    def __setitem__(self, key: RPSFWItems, value: float):
        self.values[key] = value

    def get_vals(self) -> np.ndarray:
        return self.values


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
            return
        self.utility_fn[selection] = (1 - self.lr) * self.utility_fn[selection] \
                                     + self.lr * reward
