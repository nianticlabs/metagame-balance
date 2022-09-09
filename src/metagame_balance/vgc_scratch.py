import logging
from typing import Optional

import numpy as np

from metagame_balance.Balancer import Balancer, GameEnvironment, EvaluationResult, State, StateDelta
from metagame_balance.Utility_Fn_Manager import UtilityFunctionManager
from metagame_balance.agent.Seq_Softmax_Competitor import SeqSoftmaxCompetitor
from metagame_balance.policies.CMAESBalancePolicy import CMAESBalancePolicyV2
from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.vgc.balance.Policy_Entropy_Meta import PolicyEntropyMetaData
from metagame_balance.vgc.balance.restriction import VGCDesignConstraints
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.datatypes.Objects import PkmRoster
from metagame_balance.vgc.ecosystem.BattleEcosystem import Strategy
from metagame_balance.vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from metagame_balance.vgc.util.RosterParsers import MetaRosterStateParser
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

BASE_ROSTER_SIZE = 30


class VGCState(State["VGCEnvironment"]):
    def __init__(self, policy_entropy_metadata: PolicyEntropyMetaData):
        self.policy_entropy_metadata = policy_entropy_metadata

    def encode(self) -> np.array:
        return self.policy_entropy_metadata.parser.metadata_to_state(self.policy_entropy_metadata)


class VGCStateDelta(StateDelta["VGCEnvironment"]):

    def __init__(self, delta_roster: DeltaRoster):
        self.delta_roster = delta_roster

    @classmethod
    def decode(cls, encoded: np.ndarray, state: VGCState) -> "VGCStateDelta":
        delta_roster = state.policy_entropy_metadata.parser\
            .state_to_delta_roster(encoded, state.policy_entropy_metadata)
        return cls(delta_roster)


class VGCEvaluationResult(EvaluationResult["VGCEnvironment"]):
    def __init__(self, reward: float):
        self.reward = reward

    def encode(self) -> float:
        return self.reward


def _print_roster(roster: PkmRoster):
    for p in roster:
        print(p, p.pkm_id)
        for move in p.move_roster:
            print(move.name, move.power, move.acc, move.max_pp)


class VGCEnvironment(GameEnvironment):
    def __init__(self, roster_path: Optional[str] = None, verbose: bool = True):
        # todo stupid config stuff
        n_battles = 1  # number of battles to do
        n_league_epochs = 1
        n_vgc_epochs = 1

        self.n_vgc_epochs = n_vgc_epochs
        self.n_league_epochs = n_league_epochs

        agent_names = ['agent', 'adversary']
        self.metadata = PolicyEntropyMetaData()
        self.utility_fn_manager = UtilityFunctionManager(delay_by=10)
        surrogate = [CompetitorManager(SeqSoftmaxCompetitor(a, self.utility_fn_manager)) for a in agent_names]

        if not roster_path:
            base_roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=BASE_ROSTER_SIZE).gen_roster()
        else:
            import pickle
            with open(roster_path, 'rb') as infile:
                base_roster = pickle.load(infile)

        constraints = VGCDesignConstraints(base_roster)
        if verbose:
            _print_roster(base_roster)
        self.metadata.set_moves_and_pkm(base_roster)
        reg_weights = np.ones(self.metadata.parser.length_state_vector()) / 7
        self.metadata.set_mask_weights(reg_weights)

        # this partially reimplements GameBalanceEcosystem
        self.rewards = []
        self.vgc = ChampionshipEcosystem(base_roster, self.metadata, False, False, 10, strategy=Strategy.RANDOM_PAIRING)

        for a in surrogate:
            self.vgc.register(a)

    def get_state(self) -> VGCState:
        return VGCState(self.metadata)

    def reset(self) -> VGCState:
        self.metadata.clear_stats()
        return VGCState(self.metadata)

    def get_state_bounds(self):
        return self.metadata.parser.get_state_bounds()

    def apply(self, state_delta: VGCStateDelta) -> VGCState:
        self.metadata.update_metadata(delta=state_delta.delta_roster)
        return self.get_state()

    def evaluate(self, state) -> VGCEvaluationResult:
        # train evaluator agents to convergence
        self.vgc.run(self.n_vgc_epochs, n_league_epochs=self.n_league_epochs)
        agent = next(filter(lambda a: a.competitor.name == "agent", self.vgc.league.competitors))
        self.metadata.update_metadata(policy=agent.competitor.team_build_policy)
        reward = self.metadata.evaluate()
        self.rewards.append(reward)
        return VGCEvaluationResult(reward)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    balancer = Balancer(CMAESBalancePolicyV2(), VGCEnvironment(), VGCStateDelta.decode)
    balancer.run()