from Trainer.Tabular.Abstract.Agent import *
import numpy as np


class RandomAgent(Agent):

    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.pi = [1/self.n_actions] * self.n_actions

    def check_state(self, s):
        pass

    def update(self, s0, s1, a, r, t):
        pass

    def get_action(self, s):
        """

        :param s: state
        :return: action
        """
        return np.random.choice(self.n_actions, p=self.pi)
