import numpy as np

from metagame_balance.rpsfw.util.Constants import RPSFWItems
from metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData

class RPSFWBattle():

    def __init__(self, metadata: PolicyEntropyMetaData):

        self.payoff_matrix = metadata.get_win_probs() #no longer a win rate matrix

    def battle(self, p1_choice: RPSFWItems, p2_choice: RPSFWItems):

        return self.payoff_matrix[p1_choice][p2_choice]
