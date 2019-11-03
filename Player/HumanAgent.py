from Trainer.Tabular.Abstract.Agent import *
import numpy as np


class HumanAgent(Agent):

    def __init__(self, n_actions, menu=''):
        self.n_actions = n_actions
        self.menu = menu

    def check_state(self, s):
        pass

    def update(self, s0, s1, a, r, t):
        pass

    def get_action(self, s):
        """

        :param s: state
        :return: action
        """
        return int(input(self.menu + ': ')) - 1
