from Environment.PkmBattleEnv import N_MOVES, N_SWITCHES
from Trainer.Tabular.Abstract.Agent import *
import numpy as np

SWITCH_PROBABILITY = .15


class RandomAgent(Agent):

    def __init__(self, switch_probability=SWITCH_PROBABILITY):
        super().__init__()
        self.n_actions = N_MOVES + N_SWITCHES
        self.pi = ([(1. - switch_probability) / N_MOVES] * N_MOVES) + ([switch_probability / N_SWITCHES] * N_SWITCHES)

    def get_action(self, s):
        """

        :param s: state
        :return: action
        """
        return np.random.choice(self.n_actions, p=self.pi)
