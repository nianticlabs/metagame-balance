import abc
import logging
import os
import time
from typing import TypeVar, Generic, Callable
import numpy as np
from tqdm import tqdm
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
    def apply(self, state_delta: StateDelta[G]) -> \
            "State[G]":
        """Convert an encoded state into a stateDelta, and apply it to the current game."""
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def snapshot_gameplay_policies(self, path: str):
        raise NotImplementedError

    @abc.abstractmethod
    def snapshot_game_state(self, path: str):
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


class Balancer:
    def __init__(self,
                 balance_policy: MetagameBalancePolicy,
                 game_environment: G,
                 state_delta_constructor: Callable[[np.array], StateDelta[G]],
                 snapshot_gameplay_policy_epochs: int,
                 snapshot_game_state_epochs: int,
                 snapshot_dir: str
                 ):
        self.balance_policy = balance_policy
        self.game_environment = game_environment
        self.state_delta_constructor = state_delta_constructor
        self.snapshot_gameplay_policy_epochs = snapshot_gameplay_policy_epochs
        self.snapshot_game_state_epochs = snapshot_game_state_epochs
        self.snapshot_dir = snapshot_dir

    def run(self, epochs: int):
        state = self.game_environment.reset()
        logging.info("Baseline evaluation")
        evaluation_result = self.game_environment.evaluate()

        logging.info("Starting balancer")
        
        def epoch_counter():
            _i = 0
            while _i < epochs and not self.balance_policy.converged(evaluation_result):
                yield _i
                _i += 1

        for i in tqdm(epoch_counter(), desc="balancer"):
            logging.info(f"Iteration {i}")
            tick = time.perf_counter()
            # t + 1 step
            tick_bal = time.perf_counter()
            suggestion = self.balance_policy.get_suggestion(self.game_environment, state, self.state_delta_constructor)
            self.game_environment.apply(suggestion)
            tock_bal = time.perf_counter()
            logging.info(f"iter {i} get opt: {tock_bal - tick_bal:0.2f}s")
            state = self.game_environment.get_state()
            tick_eval = time.perf_counter()
            evaluation_result = self.game_environment.evaluate()
            tock_eval = time.perf_counter()
            logging.info(f"iter {i} eval: {tock_eval - tick_eval:0.2f}s")
            tock = time.perf_counter()
            logging.info(f"iter {i} balance (total): {tock - tick:0.2f}s")

            iter_dir = os.path.join(self.snapshot_dir, f'iter_{i}')

            if i % self.snapshot_gameplay_policy_epochs == 0:
                logging.info(f"Saving gameplay policies to {iter_dir}")
                self.game_environment.snapshot_gameplay_policies(iter_dir)

            if i % self.snapshot_game_state_epochs == 0:
                logging.info(f"Saving game state to {iter_dir}")
                self.game_environment.snapshot_game_state(iter_dir)
