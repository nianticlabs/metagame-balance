from abc import ABC, abstractmethod
from typing import List

import random

from Engine.PkmBaseStructures import PkmTeam, Pkm, PkmType, PkmMove
from Engine.PkmConstants import N_MAX_PARTY, MAX_HIT_POINTS, MIN_HIT_POINTS, N_MOVES, MOVE_POWER_MAX, MOVE_POWER_MIN

LIST_OF_TYPES: List[PkmType] = list(PkmType)
DELTA_HIT_POINTS = MAX_HIT_POINTS - MIN_HIT_POINTS
DELTA_MOVE_POWER = MOVE_POWER_MAX - MOVE_POWER_MIN


class PkmTeamGenerator(ABC):

    @abstractmethod
    def get_team(self, t_id: int = 0) -> PkmTeam:
        pass

    @abstractmethod
    def fixed(self) -> bool:
        pass


# Example generators
class RandomGenerator(PkmTeamGenerator):

    def __init__(self, party_size: int = N_MAX_PARTY):
        self.party_size = party_size

    def get_team(self, t_id: int = 0) -> PkmTeam:
        team: List[Pkm] = []
        for i in range(self.party_size + 1):
            p_type: PkmType = random.choice(LIST_OF_TYPES)
            max_hp: float = round(random.random() * DELTA_HIT_POINTS + MIN_HIT_POINTS)
            moves: List[PkmMove] = []
            for _ in range(N_MOVES):
                m_type: PkmType = random.choice(LIST_OF_TYPES)
                m_power: float = round(random.random() * DELTA_MOVE_POWER + MOVE_POWER_MIN)
                moves.append(PkmMove(m_power, m_type))
            moves[0].type = p_type
            team.append(Pkm(p_type, max_hp, move0=moves[0], move1=moves[1], move2=moves[2], move3=moves[3]))
        return PkmTeam(team)

    def fixed(self) -> bool:
        return False


class FixedGenerator(PkmTeamGenerator):

    def __init__(self, gen: PkmTeamGenerator):
        self.gen: PkmTeamGenerator = gen
        self.team = [gen.get_team(0), gen.get_team(1)]

    def get_team(self, t_id: int = 0) -> PkmTeam:
        return self.team[t_id]

    def fixed(self) -> bool:
        return True
