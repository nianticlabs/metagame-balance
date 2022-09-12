from typing import Optional

import numpy as np

from metagame_balance.Balancer import Balancer, GameEnvironment, EvaluationResult, State, StateDelta
from metagame_balance.Utility_Fn_Manager import UtilityFunctionManager
from metagame_balance.agent.Seq_Softmax_Competitor import SeqSoftmaxCompetitor
from metagame_balance.policies.CMAESBalancePolicy import CMAESBalancePolicyV2
from metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData

class RSPFWState(State["RSPFWEnvironment"]):
    def __init__(self, policy_entropy_metadata: PolicyEntropyMetaData):
        self.policy_entropy_metadata = policy_entropy_metadata

    def encode(self) -> np.array:
        return self.policy_entropy_metadata.parser.metadata_to_state(self.policy_entropy_metadata)


class RSPFWStateDelta(StateDelta["RSPFWEnvironment"]):

    def __init__(self, roster: RPSFWRoster):
        self.roster = roster

    @classmethod
    def decode(cls, encoded: np.ndarray, state: RSPFWState) -> "RSPFWStateDelta":
        roster = state.policy_entropy_metadata.parser\
            .state_to_delta_roster(encoded, state.policy_entropy_metadata)
        return cls(delta_roster)


class RSPFWEvaluationResult(EvaluationResult["RSPFWEnvironment"]):

    def __init__(self, reward: float):
        self.reward = reward

    def encode(self) -> float:
        return self.reward


def _print_roster(roster: RSPFWRoster):
    for p in roster:
        print(p, p.pkm_id)
        for move in p.move_roster:
            print(move.name, move.power, move.acc, move.max_pp)


class RPSFWEnvironment(GameEnvironment):
    def __init__(self, verbose: bool = True):

        agent_names = ['agent', 'adversary']
        self.metadata = PolicyEntropyMetaData()
        self.utility_fn_manager = UtilityFunctionManager(delay_by=10)
        surrogate = [CompetitorManager(SeqSoftmaxCompetitor(a, self.utility_fn_manager)) for a in agent_names]

        if verbose:
            _print_roster(base_roster)
        reg_weights = np.ones(self.metadata.parser.length_state_vector()) / 7
        self.metadata.set_mask_weights(reg_weights)

        # this partially reimplements GameBalanceEcosystem
        self.rewards = []
        self.rpsfw = RPSFWEcosystem(self.metadata, False, False, 10)

        for a in surrogate:
            self.rpsfw.register(a)

    def get_state(self) -> RSPFWState:
        return RSPFWState(self.metadata)

    def reset(self) -> RSPFWState:
        self.metadata.clear_stats()
        return RSPFWState(self.metadata)

    def get_state_bounds(self):
        return self.metadata.parser.get_state_bounds()

    def apply(self, state_delta: RSPFWStateDelta) -> RSPFWState:
        self.metadata.update_metadata(delta=state_delta.delta_roster)
        return self.get_state()

    def evaluate(self, state) -> RSPFWEvaluationResult:
        # train evaluator agents to convergence
        self.vgc.run(self.n_vgc_epochs, n_league_epochs=self.n_league_epochs)
        agent = next(filter(lambda a: a.competitor.name == "agent", self.vgc.league.competitors))
        self.metadata.update_metadata(policy=agent.competitor.team_build_policy)
        reward = self.metadata.evaluate()
        self.rewards.append(reward)
        return RSPFWEvaluationResult(reward)

