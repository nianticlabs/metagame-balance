import logging

import matplotlib.pyplot as plt
import numpy as np

from metagame_balance.BalanceMeta import plot_rewards
from metagame_balance.Tabular_Function import TabularFn
from metagame_balance.framework import GameEnvironment, EvaluationResult, State, StateDelta
from metagame_balance.rpsfw.RPSFW_Ecosystem import RPSFWEcosystem
from metagame_balance.rpsfw.Rosters import RPSFWRoster
from metagame_balance.rpsfw.SoftmaxCompetitor import SoftmaxCompetitor
from metagame_balance.rpsfw.balance.ERG_Meta import ERGMetaData
from metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.utility import UtilityFunctionManager


class RPSFWState(State["RPSFWEnvironment"]):
    def __init__(self, policy_entropy_metadata: PolicyEntropyMetaData):
        self.policy_entropy_metadata = policy_entropy_metadata

    def encode(self) -> np.array:
        return self.policy_entropy_metadata.parser.metadata_to_state(self.policy_entropy_metadata)


class RPSFWStateDelta(StateDelta["RSPFWEnvironment"]):
    def __init__(self, delta_roster: RPSFWRoster):
        self.delta_roster = delta_roster

    @classmethod
    def decode(cls, encoded_next_state: np.ndarray, current_state: RPSFWState) -> "RPSFWStateDelta":
        delta_roster = current_state.policy_entropy_metadata.parser \
            .state_to_delta_roster(encoded_next_state, current_state.policy_entropy_metadata)
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

    def __init__(self, epochs: int, alg_baseline:bool = False,
            reg_param:int = 0,verbose: bool = True):
        agent_names = ['agent', 'adversary']

        if alg_baseline:
            self.metadata = ERGMetaData()
        else:
            self.metadata = PolicyEntropyMetaData()
        fn_approx = TabularFn(5)  # rpsfw?
        self.utility_manager = UtilityFunctionManager(fn_approx, delay_by=10)
        surrogate = []
        for a in agent_names:
            if a == "agent":
                surrogate.append(SoftmaxCompetitor(a, TabularFn(5), True, 1e-2))
            else:
                surrogate.append(SoftmaxCompetitor(a, TabularFn(5), True))

        base_roster = RPSFWRoster(self.metadata)
        if verbose:
            _print_roster(base_roster)
        reg_weights = np.ones(self.metadata.parser.length_state_vector()) * reg_param
        self.metadata.set_mask_weights(reg_weights)

        self.rewards = []
        self.entropy_vals = []
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
        # print(state.shape, self.metadata, state_delta_constructor)
        # state_delta = state_delta_constructor(state, self.metadata)
        # state_delta = state_delta_constructor(state, RPSFWState(self.metadata))
        self.metadata.update_metadata(delta=state_delta.delta_roster)
        return self.get_state()

    def evaluate(self) -> RPSFWEvaluationResult:
        # train evaluator agents to convergence
        self.rpsfw.run(self.epochs)  #  shouldn't it be a loop here?
        agent = next(filter(lambda a: a.name == "agent",
                            self.rpsfw.players))
        self.metadata.update_metadata(policy=agent)
        reward = self.metadata.evaluate()
        entropy = self.metadata.entropy()
        self.entropy_vals.append(entropy)
        self.rewards.append(reward)
        return RPSFWEvaluationResult(reward)

    def snapshot_game_state(self, path: str):
        "Don't have to do anything because this should be quick enough"
        np.save(path, np.array(self.entropy_vals))

    @property
    def last_encoded_gamestate_path(self) -> str:
        return ''

    @property
    def latest_gamestate_path(self) -> str:
        return ''

    @property
    def latest_agent_policy_path(self) -> str:
        return ''

    @property
    def latest_adversary_policy_path(self) -> str:
        return ''

    @property
    def latest_entropy_path(self) -> str:
        return ''


    def snapshot_gameplay_policies(self, path:str):
        "Don't have to do anything because this should be quick enough"
        pass

    def plot_rewards(self, path: str):
        logging.info(f"Saving rewards plot to {path}")
        logging.info(str(self.rewards))
        plot_rewards(self.rewards)
        plt.savefig(path)


    def __str__(self) -> str:
        return "RPSFW"
