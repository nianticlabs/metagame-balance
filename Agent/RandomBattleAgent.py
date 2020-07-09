from typing import List

from Engine.PkmBattleEngine import N_MOVES, N_SWITCHES
import numpy as np

from Agent.Abstract.Agent import BattleAgent

SWITCH_PROBABILITY = .15


class RandomBattleAgent(BattleAgent):

    def __init__(self, switch_probability: float = SWITCH_PROBABILITY, n_moves: int = N_MOVES,
                 n_switches: int = N_SWITCHES):
        super().__init__()
        self.n_actions: int = n_moves + n_switches
        self.pi: List[float] = ([(1. - switch_probability) / n_moves] * n_moves) + (
                    [switch_probability / n_switches] * n_switches)

    def requires_encode(self) -> bool:
        return False

    def get_action(self, s) -> int:
        """

        :param s: state
        :return: action
        """
        return np.random.choice(self.n_actions, p=self.pi)

    def close(self):
        pass
