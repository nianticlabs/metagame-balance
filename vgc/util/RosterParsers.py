from vgc.competition.StandardPkmMoves import STANDARD_MOVE_ROSTER
from vgc.balance import DeltaRoster, DeltaPkm
from vgc.balance.meta import MetaData
import copy
import numpy as np


STATS_OPT_PER_MOVE = 3
STATS_OPT_PER_PKM = 1
class MetaRosterStateParser():
    def __init__(self, num_pkm = 5, move_roster = STANDARD_MOVE_ROSTER):
        self.move_roster = move_roster
        self.num_pkm = num_pkm
        self.base_state = self.get_init_state() ## NOTE: Health is all zero!! 

    def get_init_state(self) -> np.ndarray:
        state_vec = np.zeros((STATS_OPT_PER_MOVE * len(self.move_roster) + self.num_pkm))
        for i, move in enumerate(self.move_roster):
                itr = i * 3
                state_vec[itr] = move.power
                state_vec[itr + 1] = move.acc    
                state_vec[itr + 2] = move.max_pp    
        return state_vec

    def metadata_to_state(self, meta_data: MetaData): 
        state_vec = copy.deepcopy(self.base_state)
        for pkm in meta_data._pkm: ##implement getter setter to avoid this
            
            delta_move_dict = {}
            for i, move in enumerate(pkm.move_roster):
                itr = self.move_roster.index(move) * STATS_OPT_PER_MOVE
                state_vec[itr] = move.power
                state_vec[itr + 1] = move.acc
                state_vec[itr + 2] = move.max_pp
            pkm_idx = len(self.move_roster) * STATS_OPT_PER_MOVE + pkm.pkm_id
            state_vec[pkm_idx] = pkm.max_hp
        return state_vec

    def state_to_delta_roster(self, state_vec:np.ndarray, meta_data: MetaData) -> DeltaRoster:
        
        delta_dict = {} 
        for pkm in meta_data._pkm: ##implement getter setter to avoid this
            
            delta_move_dict = {}
            for i, move in enumerate(pkm.move_roster):
                itr = self.move_roster.index(move) * STATS_OPT_PER_MOVE
                move.power = state_vec[itr]
                move.acc = state_vec[itr + 1]
                move.max_pp = state_vec[itr + 2]
                delta_move_dict[i] = move
            pkm_idx = len(self.move_roster) * STATS_OPT_PER_MOVE + pkm.pkm_id
            delta_dict[pkm.pkm_id] = DeltaPkm(state_vec[pkm_idx], pkm.type, delta_move_dict) # update max hhp here!

        return DeltaRoster(delta_dict)
