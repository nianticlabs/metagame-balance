
import numpy as np
import logging
from metagame_balance.vgc.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.vgc.datatypes.Constants import DEFAULT_TEAM_SIZE
from itertools import combinations
class ERGMetaData(PolicyEntropyMetaData):

    def __init__(self, team_size: int):

        super().__init__(team_size)


    def get_balanced_payoff(self):
        # index pay off as
        # payoff[t1p1, t1t2 .. t2p1...]
        possible_teams = list(combinations(range(len(self._pkm)), 2))
        print(possible_teams)
        payoff = np.zeros((len(possible_teams), len(possible_teams)))

        """
        for p1 in range(len(possible_teams)):
            for p2 in range(len(possible_teams)):
                if p1  == p2:
                    payoff[p1][p2] = 0
                elif p1 > p2:
                    payoff[p1][p2] = 1
                else:
                    payoff[p1][p2] = -1
        """
        return payoff

    @staticmethod
    def get_ERG(payoff:np.ndarray):
        return np.maximum(0, payoff)

    def evaluate(self, winrates) -> float:

        payoff = winrates
        expected_payoff = self.get_balanced_payoff()
        print(payoff)
        print(expected_payoff)
        """
        for t1p1 in range(len(self._pkm)):
            for t1p2 in range(len(self._pkm)):
                for t2p1 in range(len(self._pkm)):
                    for t2p2 in range(len(self._pkm)):
                        print("For team {} {} vs team {} {}: exp_payoff: {}".format(t1p1,t1p2, t2p1, t2p2, expected_payoff[t1p1][t1p2][t2p1][t2p2]))
                        #print("For team {} {} vs team {} {}: cal_payoff: {}".format(t1p1,t1p2, t2p1, t2p2, payoff[t1p1][t1p2][t2p1][t2p2]))
        """
        reward = np.sum((self.get_ERG(payoff) - self.get_ERG(expected_payoff)) ** 2)
        logging.info("\nERG=%s", str(reward))
        self.entropy()
        #logging.info("\n%s", str(self.win_probs))
        return reward
