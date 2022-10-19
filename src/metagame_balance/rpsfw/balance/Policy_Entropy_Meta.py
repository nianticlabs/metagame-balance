import logging

import numpy as np

from metagame_balance.entropy_fns import true_entropy
from metagame_balance.rpsfw.team import RPSFWTeam, predict
from metagame_balance.rpsfw.util import MetaData
from metagame_balance.rpsfw.util.Constants import RPSFWItems
from metagame_balance.rpsfw.util.Parsers import MetaRosterStateParser


class PolicyEntropyMetaData(MetaData):

    def __init__(self):
        # listings - moves, pkm, teams

        self.n_items = 5  # fixed RPSFW
        self.win_probs = np.zeros((self.n_items, self.n_items))

        self.clear_stats()
        self.current_policy = None  # I don't see another way to do, rather than taking input as P(A_j) as input in evaluate

        self.reg_weights = np.zeros((self.n_items ** 2))
        self.update_params = ['policy', 'delta']
        self.parser = MetaRosterStateParser(self.n_items)

    def set_mask_weights(self, w):
        """
        Consider adding utility functions that go like
        ``mask pkm idx, move idx etc.
        """
        self.reg_weights = w

    @staticmethod
    def get_init_win_probs(): #assume same settings!
        win_probs = np.zeros((len(RPSFWItems), len(RPSFWItems)))
        win_probs[RPSFWItems.ROCK][RPSFWItems.SCISSOR] = 1
        win_probs[RPSFWItems.ROCK][RPSFWItems.WATER] = 1
        win_probs[RPSFWItems.PAPER][RPSFWItems.WATER] = 1
        win_probs[RPSFWItems.SCISSOR][RPSFWItems.WATER] = 1
        win_probs[RPSFWItems.PAPER][RPSFWItems.ROCK] = 1
        win_probs[RPSFWItems.SCISSOR][RPSFWItems.PAPER] = 1
        win_probs[RPSFWItems.FIRE][RPSFWItems.PAPER] = 1
        win_probs[RPSFWItems.FIRE][RPSFWItems.ROCK] = 1
        win_probs[RPSFWItems.FIRE][RPSFWItems.SCISSOR] = 1
        win_probs[RPSFWItems.WATER][RPSFWItems.FIRE] = 1
        for i in range(len(win_probs)):
            for j in range(len(win_probs)):
                if i != j and win_probs[i][j] == 0:
                    win_probs[i][j] = -1
        return win_probs

    def clear_stats(self) -> None:
        self.win_probs = PolicyEntropyMetaData.get_init_win_probs()

    def update_metadata(self, **kwargs):
        assert (sum([k not in self.update_params for k in kwargs.keys()]) == 0)
        if 'delta' in kwargs.keys():
            self.update_with_delta_roster(kwargs['delta'])

        if 'policy' in kwargs.keys():
            self.update_with_policy(kwargs['policy'])
        # stage 2 policy
        # delta roster

    def update_with_policy(self, policy):

        self.current_policy = policy

    # py3.6 doesn't support the typechecking flag from future, so we will strip this annotation
    # RPSFWDeltaRoster
    def update_with_delta_roster(self, delta):
        self.win_probs = delta.roster_win_probs

    def get_win_probs(self):

        return self.win_probs

    def entropy(self):
        u = self.current_policy.get_u_fn()

        entropy_loss = true_entropy(RPSFWTeam, predict(u), 5, 1)
        #logging.info("\n\tEntropy=%s", str(entropy_loss))
        return entropy_loss


    def distance_from_init_meta(self):
        """
        Returns L2 distance from inital meta scaled with reg weights
        """

        init_win_probs = self.get_init_win_probs()
        diff = self.parser.win_probs_to_state(init_win_probs - self.win_probs)
        return ((self.reg_weights * diff) ** 2).mean(axis=0) / 100  ##something reasonable

    def evaluate(self) -> float:
        # TODO: write a function here, so that I don't have to create numpy arrays in object
        u = self.current_policy.get_u_fn()
        entropy_loss = self.entropy()
        logging.info("\n%s", str(self.win_probs))
        return entropy_loss + self.distance_from_init_meta()
