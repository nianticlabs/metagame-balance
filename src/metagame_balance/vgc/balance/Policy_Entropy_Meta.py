from copy import deepcopy
from typing import Dict, List

import numpy as np

from metagame_balance.entropy_fns import true_entropy
from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.vgc.balance.meta import MetaData, PkmId
from metagame_balance.vgc.datatypes.Constants import get_state_size
from metagame_balance.vgc.datatypes.Objects import PkmTemplate, PkmMove, PkmFullTeam, PkmRoster
from metagame_balance.vgc.team import VGCTeam, predict
from metagame_balance.vgc.util.RosterParsers import MetaRosterStateParser


class PolicyEntropyMetaData(MetaData):

    def __init__(self, team_size: int):
        # listings - moves, pkm, teams
        self.init_state = None
        self.parser = None
        self._moves: List[PkmMove] = []
        self._pkm: List[PkmTemplate] = []

        self._pkm_wins: Dict[PkmId, int] = {}
        self.current_policy = None # I don't see another way to do, rather than taking input as P(A_j) as input in evaluate

        self.reg_weights = np.zeros(())
        self.update_params = ['policy', 'delta']
        self.team_size = team_size
        self.state_dim = get_state_size(team_size)

    def set_mask_weights(self, w):
        """
        Consider adding utility functions that go like
        ``mask pkm idx, move idx etc.
        """
        self.reg_weights = w

    def set_moves_and_pkm(self, roster: PkmRoster):
        self._pkm = list(roster)
        self._moves = []
        for pkm in self._pkm:
            self._moves += list(pkm.move_roster)

        init_metadata = deepcopy(self)
        self.parser = MetaRosterStateParser(len(self._pkm))
        self.init_state = self.parser.metadata_to_state(init_metadata)
        self.init_reg_weights(self.parser.length_state_vector())

    def init_reg_weights(self, size):

        self.set_mask_weights(np.zeros(size))

    def clear_stats(self) -> None:
        for pkm in self._pkm:
            self._pkm_wins[pkm.pkm_id] = 0

    def update_with_delta_roster(self, delta: DeltaRoster):
        return

    def update_metadata(self, **kwargs):
        assert(sum([k not in self.update_params for k in kwargs.keys()]) == 0)
        if 'delta' in kwargs.keys():
            self.update_with_delta_roster(kwargs['delta'])

        if 'policy' in kwargs.keys():
            self.update_with_policy(kwargs['policy'])
        #stage 2 policy
        #delta roster

    def update_with_policy(self, policy):

        self.current_policy = policy

    def update_with_team(self, team: PkmFullTeam, won: bool):

        for pkm in team.pkm_list:
            if won:
                self._pkm_wins[pkm.pkm_id] += 1
        """
        update the meta with team if required in future
        """

    def distance_from_init_meta(self):
        """
        Returns L2 distance from inital meta scaled with reg weights
        """
        state = self.parser.metadata_to_state(self)

        return ((self.reg_weights * (state - self.init_state)) ** 2).mean(axis=0) / 100 ##something reasonable

    def to_dict(self) -> dict:
        return {
            "pokemon": [p.to_dict() for p in self._pkm]
        }

    def entropy(self) -> float:
        u = self.current_policy.get_u_fn()
        return true_entropy(VGCTeam, predict(u, self._pkm, self.state_dim, self.team_size),
                            len(self._pkm), self.team_size)

    def evaluate(self) -> float:
        # A: set of all pokemon statistics
        # does this actually need the whole policy
        # needs the winrate
        # won't sample from the policy
        # we would have to do importance sampling over the historical trajectories

        #TODO: write a function here, so that I don't have to create numpy arrays in object
        entropy_loss = self.entropy()

        return entropy_loss + self.distance_from_init_meta()
