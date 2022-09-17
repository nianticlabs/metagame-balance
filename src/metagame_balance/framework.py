import abc
import logging
from typing import TypeVar, Generic, Callable
import numpy as np
import datetime

G = TypeVar("G", bound="GameEnvironment")


class EvaluationResult(Generic[G], metaclass=abc.ABCMeta):
    # type bound encourages environment compatibility
    # could just be a wrapper for a float or something

    @abc.abstractmethod
    def encode(self) -> float:
        raise NotImplementedError


class EvaluationContext(Generic[G], metaclass=abc.ABCMeta):
    pass


class Evaluator(Generic[G], metaclass=abc.ABCMeta):
    """Evaluates a gameplay policy on its environment. This will probably need a reference to the gameplay policy,
    and receives updates on the historical performance"""
    @abc.abstractmethod
    def update(self, state_delta: "StateDelta[G]"):
        raise NotImplementedError

    def evaluate(self, state: "State[G]") -> EvaluationResult[G]:
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
    def evaluate(self) -> EvaluationResult[G]:
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
    def apply(self, state: np.ndarray, state_delta_constructor: Callable[[np.array, State[G]], StateDelta[G]]) -> "State":
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class MetagameBalancePolicy(abc.ABC):
    # should be implemented by e.g. the cma-es balance policy
    @abc.abstractmethod
    def get_suggestion(self, environment: G, state: State[G]) -> np.ndarray:
        raise NotImplementedError

    @abc.abstractmethod
    def converged(self, evaluation_result: EvaluationResult[G]) -> bool:
        # determines convergence criteria
        # - result smoothness?
        # - fixed number of steps?
        raise NotImplementedError


class Balancer:
    def __init__(self,
                 balance_policy: MetagameBalancePolicy,
                 game_environment: G,
                 state_delta_constructor: Callable[[np.array], StateDelta[G]]):
        self.balance_policy = balance_policy
        self.game_environment = game_environment
        self.state_delta_constructor = state_delta_constructor
        now = datetime.date.today()  # or whatever hte method is
        logfile = f"./logs/{game_environment}_{now.strftime('%Y%m%d_%h%m%s')}.log"
        logging.basicConfig(filename=logfile, level=logging.DEBUG)

    def run(self, epochs):
        state = self.game_environment.reset()
        evaluation_result = self.game_environment.evaluate()
        # where do I get the evaluation context from?
        i = 0
        logging.info("Starting balancer")
        while i < epochs and not self.balance_policy.converged(evaluation_result):
            logging.info(f"Iteration {i}")
            # t + 1 step
            suggestion = self.balance_policy.get_suggestion(self.game_environment, state)
            self.game_environment.apply(suggestion, self.state_delta_constructor)
            state = self.game_environment.get_state()
            evaluation_result = self.game_environment.evaluate()
            i += 1
