
import numpy as np
import logging
from metagame_balance.vgc.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.vgc.datatypes.Constants import DEFAULT_TEAM_SIZE

class ERGMetaData(PolicyEntropyMetaData):

    def get_balanced_payoff(self):
        # index pay off as
        # payoff[t1p1, t1t2 .. t2p1...]
        assert(DEFAULT_TEAM_SIZE == 2) #add more support later on
        payoff = np.ones(tuple([len(self._pkm)] * 4)) / 2

        for t1p1 in range(len(self._pkm)):
            for t1p2 in range(len(self._pkm)):
                for t2p1 in range(len(self._pkm)):
                    for t2p2 in range(len(self._pkm)):
                        if t1p1 == t1p2 or t2p2 == t2p1:
                            payoff[t1p1][t1p2][t2p1][t2p2] = 0

        return payoff

    @staticmethod
    def get_ERG(payoff:np.ndarray):
        return np.maximum(0, payoff)

    def evaluate(self, winrates) -> float:

        payoff = winrates
        expected_payoff = self.get_balanced_payoff()
        reward = np.sum((self.get_ERG(payoff) - self.get_ERG(expected_payoff)) ** 2)
        P_A, entropy_loss = self.entropy(True)
        logging.info("\nP_A=%s\tERG=%s\tEntropy=%s", str(list(P_A)), str(reward), str(entropy_loss))
        #logging.info("\n%s", str(self.win_probs))
        return reward
