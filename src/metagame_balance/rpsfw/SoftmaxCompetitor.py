import numpy as np
from scipy.special import softmax

from metagame_balance.rpsfw.Rosters import RPSFWRoster
from metagame_balance.rpsfw.util.Constants import RPSFWItems
from metagame_balance.utility import UtilityFunctionManager


class SoftmaxCompetitor:
    def __init__(self, name, utility_fn, lr: float = 1e-2):
        self.name = name
        self.utility_fn: UtilityFunctionManager = utility_fn
        self.lr = lr
        self.greedy = False

    def set_greedy(self, greedy: bool):
        self.greedy = greedy

    def get_action(self, roster: RPSFWRoster):
        values = self.utility_fn.get_vals()
        if self.greedy:
            selection_idx = np.argmax(values)
        else:
            selection_idx = np.random.choice(range(len(roster)), p=softmax(values))

        return selection_idx

    def update(self, selection: RPSFWItems, reward: float):
        self.utility_fn[selection] = (1 - self.lr) * self.utility_fn[selection] \
                                     + self.lr * reward
