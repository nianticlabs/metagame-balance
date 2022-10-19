import numpy as np
from metagame_balance.vgc.datatypes.Objects import PkmTemplate, Pkm
from metagame_balance.vgc.datatypes.Constants import STATS_OPT_2_PER_MOVE
from metagame_balance.vgc.datatypes.Constants import NUM_TYPES


def mark_with_pokemon(state, pkm, pkm_pos, state_dim: int, team_size: int):
    """
    Function marks team and the new one vector
    """

    def get_moves(pkm):
        if isinstance(pkm, PkmTemplate):
            return pkm.move_roster
        elif isinstance(pkm, Pkm):
            return pkm.moves
        else:
            raise Exception("Unrecognized pkm object type: " + str(pkm))

    def type_to_idx(type_):
        return int(type_)

    idx_to_move_stat_map = {0: lambda pkm: pkm.power, 1: lambda pkm: pkm.acc,
                            2: lambda pkm: pkm.max_pp}
    stats_per_pkm = state_dim // team_size
    base_idx = pkm_pos * stats_per_pkm
    state[base_idx] = pkm.max_hp
    state[base_idx + 1 + type_to_idx(pkm.type)] = 1
    base_idx += 1 + NUM_TYPES

    for i, move in enumerate(get_moves(pkm)):
        for j in range(len(idx_to_move_stat_map)):
            move_idx = i * STATS_OPT_2_PER_MOVE + j
            state[base_idx + move_idx] = idx_to_move_stat_map[j](move)
        state[base_idx + move_idx + type_to_idx(move.type) + 1] = 1
        # print(pkm.max_hp, pkm.type, move.power, move.acc, move.max_pp, move.type, int(move.type))
    return state


class VGCTeam():
    def __init__(self):
        self.pkms = []

    def __getitem__(self, idx: int):
        return self.pkms[idx]

    def __len__(self):
        return len(self.pkms)

    def mark(self, pkm_idx: int):
        self.pkms.append(pkm_idx)


def predict(u, pkm_list, state_dim: int, team_size: int):
    """
    U is the value function in VGC
    """
    pkm_list = pkm_list

    def batch_predictor(teams):
        x = np.zeros((len(teams), state_dim))

        for i, team in enumerate(teams):
            for j in range(len(team)):
                mark_with_pokemon(x[i], pkm_list[team[j]], j, state_dim, team_size)

        return u.predict(x)

    return batch_predictor
