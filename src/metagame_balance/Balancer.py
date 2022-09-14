import abc
import logging
from typing import TypeVar, Generic, Callable
import numpy as np

G = TypeVar("G", bound="GameEnvironment")


class EvaluationResult(Generic[G], metaclass=abc.ABCMeta):
    # type bound encourages environment compatibility
    # could just be a wrapper for a float or something

    @abc.abstractmethod
    def encode(self) -> float:
        raise NotImplementedError


class State(Generic[G], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self) -> np.array:
        raise NotImplementedError


class StateDelta(Generic[G], metaclass=abc.ABCMeta):
    # the type bound is to encourage it to be compatible with state
    @classmethod
    @abc.abstractmethod
    def decode(cls, encoded: np.ndarray, state: State[G]) -> "StateDelta[G]":
        raise NotImplementedError


class GameEnvironment(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, state: State[G]) -> EvaluationResult[G]:
        # evaluate the balance of a metagame state.
        raise NotImplementedError

    @abc.abstractmethod
    def get_state(self) -> "State[G]":
        # get the current metagame state
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self) -> "State[G]":
        # reset to some "baseline" metagame state
        raise NotImplementedError

    @abc.abstractmethod
    def get_state_bounds(self):
        raise NotImplementedError

    @abc.abstractmethod
    def apply(self, state_delta: "StateDelta") -> "State":
        raise NotImplementedError


class MetagameBalancePolicy(abc.ABC):
    # should be implemented by e.g. the cma-es balance policy
    @abc.abstractmethod
    def get_suggestion(self, environment: G, state: State[G],
                       state_delta_constructor: Callable[[np.array, State[G]], StateDelta[G]]) -> StateDelta[G]:
        raise NotImplementedError

    @abc.abstractmethod
    def converged(self, evaluation_result: EvaluationResult[G]) -> bool:
        # determines convergence criteria
        # - result smoothness?
        # - fixed number of steps?
        raise NotImplementedError


class Balancer(Generic[G]):
    # this takes the place of BalanceMeta
    def __init__(self, balance_policy: MetagameBalancePolicy,
                 game_environment: G,
                 state_delta_constructor: Callable[[np.array], StateDelta[G]]):
        self.balance_policy = balance_policy
        self.game_environment = game_environment
        self.state_delta_constructor = state_delta_constructor

    def run(self):
        state = self.game_environment.reset()
        evaluation_result = self.game_environment.evaluate(state)
        i = 0

        logging.info("Starting balancer")
        while not self.balance_policy.converged(evaluation_result):
            logging.info(f"Iteration {i}")
            # t + 1 step
            suggestion = self.balance_policy.get_suggestion(self.game_environment, state, self.state_delta_constructor)
            self.game_environment.apply(suggestion)
            state = self.game_environment.get_state()
            evaluation_result = self.game_environment.evaluate(state)
            i += 1


import argparse
from metagame_balance.rpsfw_scratch import RPSFWEnvironment, RPSFWStateDelta
from metagame_balance.rpsfw.util.Parsers import MetaRosterStateParser as RSPFWParser
from metagame_balance.vgc.util.RosterParsers import MetaRosterStateParser as VGCParser
from metagame_balance.vgc_scratch import VGCEnvironment, VGCStateDelta
from metagame_balance.policies.CMAESBalancePolicy import CMAESBalancePolicyV2

def setup_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_epochs', type=int, help='Number of updates to be done', default=1)
    parser.add_argument('--n_vgc_epochs', type=int, default=1)
    parser.add_argument('--roster_path', type=str, default='')
    parser.add_argument('--domain', type=str, default='rpsfw')
    parser.add_argument('--visualize', type=bool, default=False)
    return parser

if __name__ == "__main__":

    domain_mapper = {'rpsfw': {'env':RPSFWEnvironment, 'state-delta':RPSFWStateDelta, 'parser': RSPFWParser},
                'vgc': {'env':VGCEnvironment, 'state-delta':VGCStateDelta, 'parser': VGCParser}}
    parser = setup_argparser()
    domains = domain_mapper[parser.domain]
    balancer = Balancer(CMAESBalancePolicyV2, domains['env'], domains['parser'])
    balancer.run()
