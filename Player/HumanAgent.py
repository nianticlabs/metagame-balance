from Engine.PkmBattleEngine import N_MOVES, N_SWITCHES
from Trainer.Tabular.Abstract.Agent import *
import numpy as np


class HumanAgent(Agent):

    def __init__(self):
        self.n_actions = N_MOVES + N_SWITCHES
        self.menu = ''

    def get_action(self, s):
        """

        :param s: state
        :return: action
        """
        return int(input(self.menu + ': ')) - 1
