import numpy as np

from metagame_balance.rpsfw.util.Constants import RPSFWItems
from src.metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData

class RPSFWBattle():

    def __init__(self, metadata: PolicyEntropyMetaData):

        self.win_probs_matrix = metadata.get_win_probs()

    def battle(self, p1_choice: RPSFWItems, p2_choice: RPSFWItems):

        assert (self.win_probs_matrix[p1_choice][p2_choice] +
                self.win_probs_matrix[p2_choice][p1_choice] == 1)

        r_sam = np.random.random()
        if r_sam > self.win_probs_matrix[p1_choice][p2_choice]:
            return 0                    #P2 wins

        return 1                        #P1 wins
