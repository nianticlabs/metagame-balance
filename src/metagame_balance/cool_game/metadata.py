from metagame_balance.cool_game import BotType
import numpy as np


class CoolGameMetaData:
    def __init__(self):
        self._winrates = np.zeros((len(BotType), len(BotType)))
        # in the ERG formulation, this is a table that you take the entropy of
        # in the policy entropy case, you learn a utility function from stats onto pick slate
        self._policy = None

    @property
    def winrates(self):
        return self._winrates

    @staticmethod
    def get_init_win_probs():
        win_probs = np.zeros((len(BotType), len(BotType)))
        # ERG design matrix: cycle.
        win_probs[BotType.SAW][BotType.TORCH] = 0.7
        win_probs[BotType.NAIL][BotType.SAW] = 0.7
        win_probs[BotType.TORCH][BotType.NAIL] = 0.7

        win_probs = win_probs + -win_probs.T
        return win_probs


