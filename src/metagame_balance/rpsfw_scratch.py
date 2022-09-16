from typing import Optional

import numpy as np

from metagame_balance.framework import Balancer, GameEnvironment, EvaluationResult, State, StateDelta, Evaluator, G
from metagame_balance.utility import UtilityFunctionManager
from metagame_balance.agent.Seq_Softmax_Competitor import SeqSoftmaxCompetitor
from metagame_balance.policies.CMAESBalancePolicy import CMAESBalancePolicyV2
from metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.rpsfw.Rosters import RPSFWRoster, RPSFWDeltaRoster
from metagame_balance.rpsfw.RPSFW_Ecosystem import RPSFWEcosystem
from metagame_balance.rpsfw.SoftmaxCompetitor import SoftmaxCompetitor


class RPSFWState(State["RPSFWEnvironment"]):
    def __init__(self, policy_entropy_metadata: PolicyEntropyMetaData):
        self.policy_entropy_metadata = policy_entropy_metadata

    def encode(self) -> np.array:
        return self.policy_entropy_metadata.parser.metadata_to_state(self.policy_entropy_metadata)


class RPSFWStateDelta(StateDelta["RSPFWEnvironment"]):

    def __init__(self, roster: RPSFWRoster):
        self.roster = roster

    @classmethod
    def decode(cls, encoded: np.ndarray, state: RPSFWState) -> "RPSFWStateDelta":
        delta_roster = state.policy_entropy_metadata.parser\
            .state_to_delta_roster(encoded, state.policy_entropy_metadata)
        return cls(delta_roster)


class RPSFWEvaluationResult(EvaluationResult["RPSFWEnvironment"]):

    def __init__(self, reward: float):
        self.reward = reward

    def encode(self) -> float:
        return self.reward


def _print_roster(roster: RPSFWRoster):
    for p in roster.roster_win_probs:
        print(p)


class RPSFWEnvironment(GameEnvironment):

    def __init__(self, epochs: int, verbose: bool = True):
        agent_names = ['agent', 'adversary']
        self.metadata = PolicyEntropyMetaData()
        self.utility_fn_manager = UtilityFunctionManager(delay_by=10)
        surrogate = [SoftmaxCompetitor(a, self.utility_fn_manager) for a in agent_names]

        base_roster = RPSFWRoster(self.metadata)
        if verbose:
            _print_roster(base_roster)
        reg_weights = np.ones(self.metadata.parser.length_state_vector()) / 7
        self.metadata.set_mask_weights(reg_weights)

        # this partially reimplements GameBalanceEcosystem
        self.rewards = []
        self.rpsfw = RPSFWEcosystem(self.metadata)
        self.epochs = epochs
        for a in surrogate:
            self.rpsfw.register(a)

    def get_state(self) -> RPSFWState:
        return RPSFWState(self.metadata)

    def reset(self) -> RPSFWState:
        self.metadata.clear_stats()
        return RPSFWState(self.metadata)

    def get_state_bounds(self):
        return self.metadata.parser.get_state_bounds()

    def apply(self, state_delta: RPSFWStateDelta) -> RPSFWState:
        self.metadata.update_metadata(delta=state_delta.delta_roster)
        return self.get_state()

    def evaluate(self) -> RPSFWEvaluationResult:
        # train evaluator agents to convergence
        self.rpsfw.run(self.epochs) #### shouldn't it be a loop here?
        agent = next(filter(lambda a: a.competitor.name == "agent",
                        self.rpsfw.players))
        self.metadata.update_metadata(policy=agent.competitor.team_build_policy)
        reward = self.metadata.evaluate()
        self.rewards.append(reward)
        return RPSFWEvaluationResult(reward)

