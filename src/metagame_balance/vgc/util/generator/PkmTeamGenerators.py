import random
from abc import ABC, abstractmethod
from typing import List

import numpy as np

from metagame_balance.vgc.datatypes.Constants import MAX_HIT_POINTS, MOVE_POWER_MAX, MOVE_POWER_MIN, BASE_HIT_POINTS, \
    DEFAULT_PKM_N_MOVES, MAX_TEAM_SIZE, DEFAULT_TEAM_SIZE, DEFAULT_N_MOVES_PKM
from metagame_balance.vgc.datatypes.Objects import Pkm, PkmMove, PkmFullTeam, PkmRoster, PkmTemplate, PkmTeam
from metagame_balance.vgc.datatypes.Types import PkmType
from metagame_balance.vgc.util import softmax

LIST_OF_TYPES: List[PkmType] = list(PkmType)
DELTA_HIT_POINTS = MAX_HIT_POINTS - BASE_HIT_POINTS
DELTA_MOVE_POWER = MOVE_POWER_MAX - MOVE_POWER_MIN


class PkmTeamGenerator(ABC):

    @abstractmethod
    def get_team(self) -> PkmFullTeam:
        pass


# Example generators
class RandomTeamGenerator(PkmTeamGenerator):

    def __init__(self, party_size: int = MAX_TEAM_SIZE - 1):
        self.party_size = party_size
        self.base_stats = np.array([120., 30., 30., 30., 30.])

    def get_team(self) -> PkmFullTeam:
        team: List[Pkm] = []
        for i in range(self.party_size + 1):
            evs = np.random.multinomial(10, softmax(np.random.normal(0, 1, 5)), size=None) * 36 + self.base_stats
            p_type: PkmType = random.choice(LIST_OF_TYPES)
            max_hp: float = evs[0]
            moves: List[PkmMove] = []
            for i in range(DEFAULT_PKM_N_MOVES):
                m_type: PkmType = random.choice(LIST_OF_TYPES)
                m_power: float = evs[i + 1]
                moves.append(PkmMove(m_power, move_type=m_type))
            moves[0].type = p_type
            # random.shuffle(moves)
            team.append(Pkm(p_type, max_hp, move0=moves[0], move1=moves[1], move2=moves[2], move3=moves[3]))
        return PkmFullTeam(team)


class RandomTeamFromRoster(PkmTeamGenerator):

    def __init__(self, roster: PkmRoster, team_size=DEFAULT_TEAM_SIZE, n_moves_pkm=DEFAULT_N_MOVES_PKM):
        self.roster = list(roster)
        self.team_size = team_size
        self.n_moves_pkm = n_moves_pkm

    def get_team(self) -> PkmFullTeam:
        pkms = []
        templates: List[PkmTemplate] = random.sample(self.roster, self.team_size)
        for template in templates:
            move_combination = random.sample(range(self.n_moves_pkm), 4)
            pkms.append(template.gen_pkm(move_combination))
        return PkmFullTeam(pkms)


class RandomPkmTeam(PkmTeam):

    def __init__(self, team_gen: PkmTeamGenerator, size=3):
        super().__init__()
        self.gen: PkmTeamGenerator = team_gen
        self.reset()
        self.size = size

    def reset(self):
        self.reset_team_members(self.gen.get_team().pkm_list)
