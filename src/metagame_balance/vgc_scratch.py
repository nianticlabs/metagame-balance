import json
import logging
import os.path
from typing import Optional, List

import matplotlib.pyplot as plt
import numpy as np
import torch

from metagame_balance.BalanceMeta import plot_rewards
from metagame_balance.FCNN import FCNN
from metagame_balance.agent.Seq_Softmax_Competitor import SeqSoftmaxCompetitor
from metagame_balance.evaluate.approximate_entropy import APEState, GamePolicy
from metagame_balance.framework import GameEnvironment, EvaluationResult, StateDelta, \
    G
from metagame_balance.utility import UtilityFunctionManager
from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.vgc.balance.ERG_Meta import ERGMetaData
from metagame_balance.vgc.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.datatypes.Constants import DEFAULT_TEAM_SIZE, get_state_size
from metagame_balance.vgc.datatypes.Objects import PkmRoster
from metagame_balance.vgc.ecosystem.BattleEcosystem import Strategy
from metagame_balance.vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

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
    @property
    def latest_gamestate_path(self):
        return self._latest_gamestate_path

    @property
    def latest_agent_policy_path(self):
        return self._latest_agent_policy_path

    @property
    def latest_adversary_policy_path(self):
        return self._latest_adversary_policy_path

    @property
    def latest_entropy_path(self):
        return self._latest_entropy_path

    def plot_rewards(self, path: str):
        logging.info(f"Saving rewards plot to {path}")
        logging.info(str(self.rewards))
        plot_rewards(self.rewards)
        plt.savefig(path)

    def snapshot_game_state(self, path: str):
        """Save the game state into """
        state_dict = self.metadata.to_dict()
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "game_state.json"), "w") as outfile:
            self._latest_gamestate_path = os.path.join(path, "game_state.json")
            json.dump(state_dict, outfile)
        np.save(os.path.join(path, "entropies.npy"), np.array(self.entropy_vals))
        self._latest_entropy_path = os.path.join(path, "entropies.npy")

    def snapshot_gameplay_policies(self, path: str):
        """Snapshot the teampickers - agent and adversary"""
        os.makedirs(path, exist_ok=True)
        torch.save(self.utility_fn_manager.agent_U_function().state_dict(),
                   os.path.join(path, "agent.pt"))
        self._latest_agent_policy_path = os.path.join(path, "agent.pt")
        torch.save(self.utility_fn_manager.adversary_U_function().state_dict(),
                   os.path.join(path, "adversary.pt"))
        self._latest_adversary_policy_path = os.path.join(path, "adversary.pt")

    def __init__(self,
                 team_size: int,
                 roster_path: Optional[str] = None, verbose: bool = True,
                 n_league_epochs: int = 10, n_battles_per_league: int = 10,
                 reg_param: float = 0, alg_baseline: bool = False,
                 ):
        self._latest_gamestate_path = None
        self._latest_agent_policy_path = None
        self._latest_adversary_policy_path = None
        self._latest_entropy_path = None

        n_vgc_epochs = n_battles_per_league

        # number of championships to run
        self.n_vgc_epochs = n_vgc_epochs

        # number of battles in a championship

        self.n_league_epochs = n_league_epochs

        agent_names = ['agent', 'adversary']

        self.alg_baseline = alg_baseline
        if alg_baseline:
            self.metadata = ERGMetaData(team_size)
        else:
            self.metadata = PolicyEntropyMetaData(team_size)
        self.team_size = team_size
        init_nn = FCNN([get_state_size(team_size), 128, 64, 1])
        init_nn.compile()  # consider using SGD over Adam

        self.utility_fn_manager = UtilityFunctionManager(init_nn, delay_by=10)
        surrogate = [CompetitorManager(SeqSoftmaxCompetitor(a, self.utility_fn_manager, team_size))
                     for a in agent_names]

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
        self.entropy_vals: List[float] = []
        self.vgc = ChampionshipEcosystem(base_roster, self.metadata, False, False, strategy=Strategy.RANDOM_PAIRING,
                                         team_size=team_size)

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
        self.vgc.run(self.n_vgc_epochs, n_league_epochs=self.n_league_epochs) #required to calculate entropy
        agent = next(filter(lambda a: a.competitor.name == "agent", self.vgc.league.competitors))
        self.metadata.update_metadata(policy=agent.competitor.team_build_policy)

        if self.alg_baseline:
            win_rates = self.sample_payoff()
            reward = self.metadata.evaluate(win_rates)
            entropy = self.metadata.entropy()
        else:
            reward = self.metadata.evaluate()
            entropy = reward
        self.entropy_vals.append(entropy)
        logging.info(f"metadata reward: {reward}")
        self.rewards.append(reward)
        return VGCEvaluationResult(reward)

    def sample_payoff(self):
        logging.info("Simulating sample payoff")
        assert (DEFAULT_TEAM_SIZE == 2)  # add more support later on
        num_pkm = len(self.metadata._pkm)
        payoff = np.zeros(tuple([num_pkm] * 4))
        t1 = []
        t2 = []
        for t1p1 in range(num_pkm):
            for t1p2 in range(num_pkm):
                for t2p1 in range(num_pkm):
                    for t2p2 in range(num_pkm):
                        if t1p1 == t1p2 or t2p2 == t2p1 or payoff[t1p1][t1p2][t2p1][t2p2] != 0:
                            continue
                        t1 = [t1p1, t1p2]
                        t2 = [t2p1, t2p2]
                        win_prob = self.vgc.simulate_n_battles(1, t1, t2)
                        payoff[t1p1][t1p2][t2p1][t2p2] = win_prob
                        payoff[t2p1][t2p2][t1p1][t1p2] = 1 - win_prob
        return payoff

    def __str__(self) -> str:
        return "VGC"
