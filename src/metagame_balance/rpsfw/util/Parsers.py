import numpy as np
from typing import Tuple
import copy
from metagame_balance.rpsfw.Rosters import RPSFWDeltaRoster
from metagame_balance.rpsfw.util import MetaData


class MetaRosterStateParser:
    def __init__(self, num_items):
        """
        state vector [move_id_1_feat_1, move_id_1_feat_2, .. move_id_2_feat1, .... pkm_1_feat_1, pkm_1_feat_2, ..]
        """
        self.num_items = num_items

    def length_state_vector(self) -> int:
        """
        all the pairwise relationships between choices
        """
        return int(((self.num_items + 1) * self.num_items) / 2)

    def get_normalization_vector(self) -> np.ndarray:
        """
        Get max of each position for normalization
        """
        max_vec = np.ones((self.length_state_vector()))
        return max_vec

    def get_state_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        return np.zeros((self.length_state_vector())), \
                np.ones((self.length_state_vector()))

    def metadata_to_state(self, meta_data: MetaData) -> np.ndarray:
        """
        Takes meta data, uses _pkm and _moves to convert into a state vector
        """
        win_probs = meta_data.get_win_probs()
        return self.win_probs_to_state(win_probs)

    def win_probs_to_state(self, win_probs):
        state_vec = np.zeros(self.length_state_vector())
        ctr = 0
        for i in range(self.num_items):
            for j in range(i + 1, self.num_items):
                state_vec[ctr] = win_probs[i][j]
                ctr += 1
        return state_vec

    def state_to_delta_roster(self, state_vec: np.ndarray,
                              meta_data: MetaData) -> RPSFWDeltaRoster:
        """
        Takes state vector and creates delta roster accordingly
        """
        win_probs = copy.deepcopy(meta_data.get_win_probs())
        ctr = 0
        for i in range(self.num_items):
            for j in range(i + 1, self.num_items):
                win_probs[i][j] = state_vec[ctr]
                ctr += 1

        return RPSFWDeltaRoster(win_probs)
