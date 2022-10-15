import abc
from typing import Generic

import numpy as np
from scipy.stats import entropy

from metagame_balance.framework import G, StateDelta, EvaluationResult, State


# class GamePolicy(Generic[G], metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def optimal_pick(self) -> np.ndarray:
#         """Returns the average amount of times each action is picked."""
#         raise NotImplementedError


# class ApproximatePolicyEntropyEvaluationContext(EvaluationContext[G], metaclass=abc.ABCMeta):
#     """This needs to be implemented wrt a specific game environment"""
#     @property
#     @abc.abstractmethod
#     def policy(self) -> GamePolicy[G]:
#         raise NotImplementedError

# class APEState(State[G]):
#     @property
#     @abc.abstractmethod
#     def policy(self) -> GamePolicy[G]:
#         raise NotImplementedError
#
#
# class APEEvaluationResult(EvaluationResult[G]):
#     def encode(self) -> float:
#         return self._entropy
#
#     def __init__(self, entropy: float):
#         self._entropy = entropy
#
#
# class ApproximatePolicyEntropyEvaluator(Evaluator[G], metaclass=abc.ABCMeta):
#     """Evaluates a policy."""
#
#     def evaluate(self, state: APEState[G]) -> EvaluationResult[G]:
#         return APEEvaluationResult(-entropy(state.policy.optimal_pick()))
#
#     @abc.abstractmethod
#     def update(self, state_delta: "StateDelta[G]"):
#         raise NotImplementedError





