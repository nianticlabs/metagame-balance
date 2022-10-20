import abc
import atexit
import logging
import os
import time
from typing import TypeVar, Generic, Callable, Optional

import matplotlib
import numpy as np
import numpy.typing as npt
from tqdm import tqdm
import datetime

G = TypeVar("G", bound="GameEnvironment")


class EvaluationResult(Generic[G], metaclass=abc.ABCMeta):
    # type bound encourages environment compatibility
    # could just be a wrapper for a float or something

    @abc.abstractmethod
    def encode(self) -> float:
        """
        convert the internal representation of this game's evaluation result into a scalar.

        This will be maximized by the balancer.
        """
        raise NotImplementedError


class State(Generic[G], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self) -> npt.NDArray:
        raise NotImplementedError


class StateDelta(Generic[G], metaclass=abc.ABCMeta):
    # the type bound is to encourage it to be compatible with state
    @classmethod
    @abc.abstractmethod
    def decode(cls, encoded_next_state: npt.NDArray, current_state: State[G]) -> "StateDelta[G]":
        """
        Given an encoded state, create a statedelta. In a lot of cases, you can just wrap the new state in this class
        and unwrap / apply it in downstream steps.
        """
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
        """Convert an encoded state into a stateDelta, and apply it to the current game. Return the new state."""
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

    @abc.abstractmethod
    def plot_rewards(self, path: str):
        """Plot the environment's reward history to a file at the given prefix. This will be called atexit by
        the balancer."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def last_encoded_gamestate_path(self) -> str:
        pass


    @property
    @abc.abstractmethod
    def latest_gamestate_path(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def latest_agent_policy_path(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def latest_adversary_policy_path(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def latest_entropy_path(self) -> str:
        pass




class MetagameBalancePolicy(abc.ABC):
    # should be implemented by e.g. the cma-es balance policy
    @abc.abstractmethod
    def get_suggestion(self, environment: G, state: State[G],
                       state_delta_constructor: Callable[[npt.NDArray, State[G]], StateDelta[G]],
                       evaluation_result: EvaluationResult[G]) -> StateDelta[G]:
        raise NotImplementedError

    @abc.abstractmethod
    def converged(self, evaluation_result: Optional[EvaluationResult[G]]) -> bool:
        # determines convergence criteria
        # - result smoothness?
        # - fixed number of steps?
        raise NotImplementedError


class Balancer(Generic[G]):
    def __init__(self,
                 balance_policy: MetagameBalancePolicy,
                 game_environment: G,
                 state_delta_constructor: Callable[[npt.NDArray, State[G]], StateDelta[G]],
                 snapshot_gameplay_policy_epochs: int,
                 snapshot_game_state_epochs: int,
                 experiment_dir: str
                 ):
        self.balance_policy = balance_policy
        self.game_environment = game_environment
        self.state_delta_constructor = state_delta_constructor
        self.snapshot_gameplay_policy_epochs = snapshot_gameplay_policy_epochs
        self.snapshot_game_state_epochs = snapshot_game_state_epochs
        self.experiment_dir = experiment_dir
        os.makedirs(experiment_dir, exist_ok=True)
        matplotlib.use("Agg")  # do not create a plot window when trying to exit
        self.rewards_path = os.path.join(self.experiment_dir, "rewards.png")
        atexit.register(self.game_environment.plot_rewards, self.rewards_path)

    def run(self, epochs: int):
        self.game_environment.reset()
        logging.info("Starting balancer")

        evaluation_result: Optional[EvaluationResult[G]] = None
        
        def epoch_counter():
            _i = 0
            while _i <= epochs and not self.balance_policy.converged(evaluation_result):
                yield _i
                _i += 1

        for i in tqdm(epoch_counter(), desc="balancer"):
            logging.info(f"Iteration {i}")
            tick = time.perf_counter()

            tick_eval = time.perf_counter()
            evaluation_result = self.game_environment.evaluate()  # expensive
            tock_eval = time.perf_counter()
            logging.info(f"iter {i} eval: {tock_eval - tick_eval:0.2f}s")
            tock = time.perf_counter()

            # t + 1 step
            tick_bal = time.perf_counter()
            state: State[G] = self.game_environment.get_state()
            suggestion = self.balance_policy.get_suggestion(self.game_environment, state, self.state_delta_constructor,
                                                            evaluation_result)
            self.game_environment.apply(suggestion)
            tock_bal = time.perf_counter()
            logging.info(f"iter {i} get opt: {tock_bal - tick_bal:0.2f}s")

            logging.info(f"iter {i} balance (total): {tock - tick:0.2f}s")

            iter_dir = os.path.join(self.experiment_dir, f'iter_{i}')

            if i % self.snapshot_gameplay_policy_epochs == 0:
                logging.info(f"Saving gameplay policies to {iter_dir}")
                os.makedirs(iter_dir, exist_ok=True)
                self.game_environment.snapshot_gameplay_policies(iter_dir)

            if i % self.snapshot_game_state_epochs == 0:
                logging.info(f"Saving game state to {iter_dir}")
                os.makedirs(iter_dir, exist_ok=True)
                self.game_environment.snapshot_game_state(iter_dir)

        self.game_environment.plot_rewards(self.rewards_path)
