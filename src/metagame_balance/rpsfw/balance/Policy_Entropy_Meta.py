from abc import ABC, abstractmethod
from math import exp
from typing import Dict, List
from scipy.stats import entropy
from scipy.special import softmax
from copy import deepcopy
#from vgc.util.RosterParsers import MetaRosterStateParser
from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.rpsfw.util.RosterParsers import MetaRosterStateParser
from metagame_balance.rpsfw.util.Constants import RPSFWItems
import numpy as np

class MetaData():

    @abstractmethod
    def clear_stats(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_metadata(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def evaluate(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_win_probs(self):
        raise NotImplementedError

class PolicyEntropyMetaData(MetaData):

    def __init__(self):
        # listings - moves, pkm, teams

        self.items = 5 #fixed RPSFW
        self.win_probs = np.zeros((self.items, self.items))

        self.clear_stats()
        self.current_policy = None # I don't see another way to do, rather than taking input as P(A_j) as input in evaluate

        self.reg_weights = np.zeros((self.items ** 2))
        self.update_params = ['policy', 'delta']
        self.parser = MetaRosterStateParser()

    def set_mask_weights(self, w):
        """
        Consider adding utility functions that go like
        ``mask pkm idx, move idx etc.
        """
        self.reg_weights = w

    def clear_stats(self) -> None:

        self.win_probs[RPSFWItems.ROCK][RPSFWItems.SCISSOR] = 1
        self.win_probs[RPSFWItems.PAPER][RPSFWItems.ROCK] = 1
        self.win_probs[RPSFWItems.SCISSOR][RPSFWItems.PAPER] = 1
        self.win_probs[RPSFWItems.FIRE][RPSFWItems.PAPER] = 1
        self.win_probs[RPSFWItems.FIRE][RPSFWItems.ROCK] = 1
        self.win_probs[RPSFWItems.FIRE][RPSFWItems.SCISSOR] = 1
        self.win_probs[RPSFWItems.WATER][RPSFWItems.FIRE] = 1

    def update_metadata(self, **kwargs):

        assert(sum([k not in self.update_params for k in kwargs.keys()]) == 0)
        if 'delta' in kwargs.keys():
            self.update_with_delta_roster(kwargs['delta'])

        if 'policy' in kwargs.keys():
            self.update_with_policy(kwargs['policy'])
        #stage 2 policy
        #delta roster

    def update_with_policy(self, policy):

        self.current_policy = policy

    def update_with_delta_roster(self, delta: DeltaRoster):

        self.win_probs = delta.get_win_probs()

    def get_win_probs(self):

        return self.win_probs

    def distance_from_init_meta(self):
        """
        Returns L2 distance from inital meta scaled with reg weights
        """
        state = self.parser.metadata_to_state(self)

        return ((self.reg_weights * (state - self.init_state)) ** 2).mean(axis=0) / 100 ##something reasonable


    def evaluate(self) -> float:
        #TODO: write a function here, so that I don't have to create numpy arrays in object
        A = np.zeros((len(self._pkm), STAGE_2_STATE_DIM))

        for i, pkm in enumerate(self._pkm):
            self.current_policy._mark(A[i], [], pkm)
        u = self.current_policy.get_u_fn()
        P_A = softmax(u.predict(A))

        print(P_A)
        entropy_loss = -entropy(P_A)
        return entropy_loss + self.distance_from_init_meta()
