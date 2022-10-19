import copy
from typing import Tuple

import numpy as np

from metagame_balance.vgc.balance import DeltaRoster, DeltaPkm
from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.competition.StandardPkmMoves import STANDARD_MOVE_ROSTER
from metagame_balance.vgc.datatypes.Constants import STATS_OPT_1_PER_MOVE, MAX_MOVE_POWER, MAX_MOVE_ACC, \
    MAX_MOVE_MAX_PP, MAX_PKM_HP


class MetaRosterStateParser:

    def __init__(self, num_pkm, consider_hp=False, move_roster=STANDARD_MOVE_ROSTER):
        """
        state vector [move_id_1_feat_1, move_id_1_feat_2, .. move_id_2_feat1, .... pkm_1_feat_1, pkm_1_feat_2, ..]
        """
        self.move_roster = move_roster
        self.num_pkm = num_pkm
        self.consider_hp = consider_hp
        self.base_state = self.get_init_state()   # NOTE: Health is all zero!!
        self.norm_vec = self.get_normalization_vector()

    def length_state_vector(self):
        """
        Returns length of state vector
        """
        moves_length = STATS_OPT_1_PER_MOVE * len(self.move_roster)
        if self.consider_hp:
            return moves_length + self.num_pkm
        else:
            return moves_length

    def get_init_state(self) -> np.ndarray:
        """
        Get initial state based on move
        Note: Pokemon stats set to zero, as they are unavailable in init
        """
        state_vec = np.zeros((self.length_state_vector()))
        for i, move in enumerate(self.move_roster):
            itr = i * 3
            state_vec[itr] = move.power
            state_vec[itr + 1] = move.acc
            state_vec[itr + 2] = move.max_pp
        return state_vec

    def get_normalization_vector(self) -> np.ndarray:
        """
        Get max of each position for normalization
        """
        max_vec = np.zeros((self.length_state_vector()))
        power_idxs = [i * 3 for i in range(len(self.move_roster))]
        acc_idxs = [i * 3 + 1 for i in range(len(self.move_roster))]
        max_pp_idxs = [i * 3 + 2 for i in range(len(self.move_roster))]
        health_idxs = [i for i in range(len(self.move_roster) * 3, len(max_vec))]
        max_vec[power_idxs] = MAX_MOVE_POWER
        max_vec[acc_idxs] = MAX_MOVE_ACC
        max_vec[max_pp_idxs] = MAX_MOVE_MAX_PP
        max_vec[health_idxs] = MAX_PKM_HP
        return max_vec

    def get_state_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        return np.zeros((self.length_state_vector())), np.ones((self.length_state_vector()))

    def metadata_to_state(self, meta_data: MetaData) -> np.ndarray:
        """
        Takes meta data, uses _pkm and _moves to convert into a state vector
        """
        state_vec = copy.deepcopy(self.base_state)
        for pkm in meta_data._pkm:  ## implement getter setter to avoid this

            delta_move_dict = {}
            for i, move in enumerate(pkm.move_roster):
                itr = self.move_roster.index(move) * STATS_OPT_1_PER_MOVE
                state_vec[itr] = move.power
                state_vec[itr + 1] = move.acc
                state_vec[itr + 2] = move.max_pp
                # print(state_vec[itr:itr+3], self.norm_vec[itr:itr+3], itr)
                assert ((state_vec[itr:itr + 3] <= self.norm_vec[itr:itr + 3]).all())
            if self.consider_hp:
                pkm_idx = len(self.move_roster) * STATS_OPT_1_PER_MOVE + pkm.pkm_id
                state_vec[pkm_idx] = max(1, np.round(pkm.max_hp))  # Make sure an HP of atleast 1
        return state_vec / self.norm_vec

    def state_to_delta_roster(self, state_vec: np.ndarray, meta_data: MetaData) -> DeltaRoster:
        """
        Takes state vector and creates delta roster accordingly
        """
        state_vec = state_vec * self.norm_vec
        delta_dict = {}
        for pkm in meta_data._pkm:  ##implement getter setter to avoid this

            delta_move_dict = {}
            for i, move in enumerate(pkm.move_roster):
                itr = self.move_roster.index(move) * STATS_OPT_1_PER_MOVE
                move.power = state_vec[itr]
                move.acc = state_vec[itr + 1]
                move.max_pp = state_vec[itr + 2]
                delta_move_dict[i] = move
            if self.consider_hp:
                pkm_idx = len(self.move_roster) * STATS_OPT_1_PER_MOVE + pkm.pkm_id  ### get idx of pokemon HP from here
                hp = max(1, np.round(state_vec[pkm_idx]))
            else:
                hp = pkm.max_hp
            delta_dict[pkm.pkm_id] = DeltaPkm(hp, pkm.type, delta_move_dict)  # update max hhp here!

        return DeltaRoster(delta_dict)
