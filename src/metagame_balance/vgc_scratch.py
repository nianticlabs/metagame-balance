import json
import logging
import os.path
from typing import Optional, Callable, List

import matplotlib.pyplot as plt
import numpy as np
import torch

from metagame_balance.BalanceMeta import plot_rewards
from metagame_balance.utility import UtilityFunctionManager
from metagame_balance.agent.Seq_Softmax_Competitor import SeqSoftmaxCompetitor
from metagame_balance.evaluate.approximate_entropy import ApproximatePolicyEntropyEvaluator, APEState, GamePolicy
from metagame_balance.framework import Balancer, GameEnvironment, EvaluationResult, StateDelta, \
    G, Evaluator, State
from metagame_balance.policies.CMAESBalancePolicy import CMAESBalancePolicyV2
from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.vgc.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.vgc.balance.restriction import VGCDesignConstraints
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.datatypes.Objects import PkmRoster
from metagame_balance.vgc.ecosystem.BattleEcosystem import Strategy
from metagame_balance.vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from metagame_balance.FCNN import FCNN
from metagame_balance.vgc.datatypes.Constants import STAGE_2_STATE_DIM

BASE_ROSTER_SIZE = 30


class VGCGameplayPolicy(GamePolicy["VGCEnvironment"]):
    def __init__(self, metadata: PolicyEntropyMetaData):
        self._metadata = metadata

    def optimal_pick(self) -> np.ndarray:
        # self._metadata.
        raise NotImplementedError


class VGCState(APEState["VGCEnvironment"]):
    @property
    def policy(self) -> GamePolicy[G]:
        self.policy_entropy_metadata.current_policy

    def __init__(self, policy_entropy_metadata: PolicyEntropyMetaData):
        self.policy_entropy_metadata = policy_entropy_metadata

    def encode(self) -> np.array:
        return self.policy_entropy_metadata.parser.metadata_to_state(self.policy_entropy_metadata)


class VGCStateDelta(StateDelta["VGCEnvironment"]):
    def __init__(self, delta_roster: DeltaRoster):
        self.delta_roster = delta_roster

    @classmethod
    def decode(cls, encoded: np.ndarray, state: VGCState) -> "VGCStateDelta":
        delta_roster = state.policy_entropy_metadata.parser \
            .state_to_delta_roster(encoded, state.policy_entropy_metadata)
        return cls(delta_roster)


class VGCEvaluationResult(EvaluationResult["VGCEnvironment"]):
    def __init__(self, reward: float):
        self.reward = reward

    def encode(self) -> float:
        return self.reward


def _print_roster(roster: PkmRoster):
    for p in roster:
        logging.info(p, p.pkm_id)
        for move in p.move_roster:
            logging.info(move.name, move.power, move.acc, move.max_pp)


class VGCEnvironment(GameEnvironment):
    def plot_rewards(self, path: str):
        logging.info(f"Saving rewards plot to {path}")
        logging.info(str(self.rewards))
        plot_rewards(self.rewards)
        plt.savefig(path)

    def snapshot_game_state(self, path: str):
        state_dict = self.metadata.to_dict()
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "game_state.json"), "w") as outfile:
            json.dump(state_dict, outfile)

    def snapshot_gameplay_policies(self, path: str):
        """Snapshot the teampickers - agent and adversary"""
        os.makedirs(path, exist_ok=True)
        torch.save(self.utility_fn_manager.agent_U_function().state_dict(),
                   os.path.join(path, "agent.pt"))
        torch.save(self.utility_fn_manager.adversary_U_function().state_dict(),
                   os.path.join(path, "adversary.pt"))

    def __init__(self, roster_path: Optional[str] = None, verbose: bool = True,
            n_league_epochs: int = 10, n_battles_per_league: int = 10, reg_param: float = 0):
        # todo stupid config stuff
        n_vgc_epochs = 1

        # number of championships to run
        self.n_vgc_epochs = n_vgc_epochs

        # number of battles in a championship

        self.n_league_epochs = n_league_epochs

        agent_names = ['agent', 'adversary']
        self.metadata = PolicyEntropyMetaData()
        input_dim = STAGE_2_STATE_DIM
        init_nn = FCNN([input_dim, 128, 64, 1])
        init_nn.compile()  # consider using SGD over Adam

        self.utility_fn_manager = UtilityFunctionManager(init_nn, delay_by=10)
        surrogate = [CompetitorManager(SeqSoftmaxCompetitor(a, self.utility_fn_manager)) for a in agent_names]

        if not roster_path:
            base_roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=BASE_ROSTER_SIZE).gen_roster()
        else:
            import pickle
            with open(roster_path, 'rb') as infile:
                base_roster = pickle.load(infile)

        if verbose:
            _print_roster(base_roster)
        self.metadata.set_moves_and_pkm(base_roster)
        reg_weights = np.ones(self.metadata.parser.length_state_vector()) * reg_param
        self.metadata.set_mask_weights(reg_weights)

        # this partially reimplements GameBalanceEcosystem
        self.rewards: List[float] = []
        self.vgc = ChampionshipEcosystem(base_roster, self.metadata, False, False, n_battles_per_league,
                                         strategy=Strategy.RANDOM_PAIRING)

        for a in surrogate:
            self.vgc.register(a)

    def get_state(self) -> VGCState:
        return VGCState(self.metadata)

    def reset(self) -> VGCState:
        self.metadata.clear_stats()
        return VGCState(self.metadata)

    def get_state_bounds(self):
        return self.metadata.parser.get_state_bounds()

    def apply(self, state_delta: VGCStateDelta) -> \
            VGCState:
        self.metadata.update_metadata(delta=state_delta.delta_roster)
        return self.get_state()

    def evaluate(self) -> VGCEvaluationResult:
        # train evaluator agents to convergence
        self.vgc.run(self.n_vgc_epochs, n_league_epochs=self.n_league_epochs)
        agent = next(filter(lambda a: a.competitor.name == "agent", self.vgc.league.competitors))
        self.metadata.update_metadata(policy=agent.competitor.team_build_policy)
        reward = self.metadata.evaluate()
        logging.info(f"metadata reward: {reward}")
        self.rewards.append(reward)
        return VGCEvaluationResult(reward)

    def __str__(self) -> str:
        return "VGC"
