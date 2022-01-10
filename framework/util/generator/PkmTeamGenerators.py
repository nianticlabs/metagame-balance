import random
from abc import ABC, abstractmethod
from typing import List

from framework.datatypes.Constants import MAX_HIT_POINTS, MOVE_POWER_MAX, MOVE_POWER_MIN, MIN_HIT_POINTS, \
    DEFAULT_PKM_N_MOVES, MAX_TEAM_SIZE
from framework.datatypes.Objects import Pkm, PkmMove, PkmFullTeam, PkmRoster, PkmTemplate
from framework.datatypes.Types import PkmType

LIST_OF_TYPES: List[PkmType] = list(PkmType)
DELTA_HIT_POINTS = MAX_HIT_POINTS - MIN_HIT_POINTS
DELTA_MOVE_POWER = MOVE_POWER_MAX - MOVE_POWER_MIN


class PkmTeamGenerator(ABC):

    @abstractmethod
    def get_team(self, t_id: int = 0) -> PkmFullTeam:
        pass


# Example generators
class RandomGenerator(PkmTeamGenerator):

    def __init__(self, party_size: int = MAX_TEAM_SIZE - 1):
        self.party_size = party_size

    def get_team(self, t_id: int = 0) -> PkmFullTeam:
        team: List[Pkm] = []
        for i in range(self.party_size + 1):
            p_type: PkmType = random.choice(LIST_OF_TYPES)
            max_hp: float = round(random.random() * DELTA_HIT_POINTS + MIN_HIT_POINTS)
            moves: List[PkmMove] = []
            for _ in range(DEFAULT_PKM_N_MOVES):
                m_type: PkmType = random.choice(LIST_OF_TYPES)
                m_power: float = round(random.random() * DELTA_MOVE_POWER + MOVE_POWER_MIN)
                moves.append(PkmMove(m_power, 1., m_type))
            moves[0].type = p_type
            random.shuffle(moves)
            team.append(Pkm(p_type, max_hp, move0=moves[0], move1=moves[1], move2=moves[2], move3=moves[3]))
        return PkmFullTeam(team)


class RandomGeneratorRoster:

    def __init__(self, roster: PkmRoster):
        self.roster = list(roster)

    def get_team(self, size=6) -> PkmFullTeam:
        pkms = []
        templates: List[PkmTemplate] = random.sample(self.roster, size)
        for template in templates:
            move_combination = random.sample(range(10), 4)
            pkms.append(template.gen_pkm(move_combination))
        return PkmFullTeam(pkms)
