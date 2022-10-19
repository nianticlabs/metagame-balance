from metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.rpsfw.util.Constants import RPSFWItems


class RPSFWBattle():

    def __init__(self, metadata: PolicyEntropyMetaData):

        self.metadata = metadata

    def battle(self, p1_choice: RPSFWItems, p2_choice: RPSFWItems):

        payoff_matrix = self.metadata.get_win_probs() #no longer a win rate matrix
        return payoff_matrix[p1_choice][p2_choice]
