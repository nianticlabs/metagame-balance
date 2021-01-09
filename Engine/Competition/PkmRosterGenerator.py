from abc import ABC, abstractmethod
from Engine.DataObjects import PkmType, PkmMove, PkmRoster, PkmMoveRoster, PkmTemplate
from Engine.DataConstants import MIN_HIT_POINTS, MOVE_POWER_MIN
from Engine.StandardPkmMoves import STANDARD_MOVE_POOL
from Engine.Competition.PkmTeamGenerator import LIST_OF_TYPES, DELTA_HIT_POINTS, DELTA_MOVE_POWER
import random


class PkmPoolGenerator(ABC):

    @abstractmethod
    def get_pool(self) -> PkmRoster:
        pass


class StandardPkmPoolGenerator(PkmPoolGenerator):

    def __init__(self, n_moves_pkm: int, pool_size: int):
        self.move_pool: PkmMoveRoster = STANDARD_MOVE_POOL
        self.n_moves_pkm = n_moves_pkm
        self.pool_size = pool_size

    def get_pool(self) -> PkmRoster:
        pool: PkmRoster = []
        for i in range(self.pool_size):
            base_move_pool = self.move_pool.copy()
            p_type: PkmType = random.choice(LIST_OF_TYPES)
            max_hp: float = round(random.random() * DELTA_HIT_POINTS + MIN_HIT_POINTS)
            moves = random.sample(list(filter(lambda _m: _m.type == p_type, base_move_pool)), 2)
            for m in moves:
                base_move_pool.remove(m)
            move_pool: PkmMoveRoster = moves
            for _ in range(self.n_moves_pkm - 1):
                if random.random() < .2:
                    m_type: PkmType = random.choice(LIST_OF_TYPES)
                    m_power: float = round(random.random() * DELTA_MOVE_POWER + MOVE_POWER_MIN)
                    move = PkmMove(power=m_power, move_type=m_type)
                else:
                    move = random.choice(base_move_pool)
                    base_move_pool.remove(move)
                move_pool.append(move)
            random.shuffle(move_pool)
            pool.append(PkmTemplate(move_pool, p_type, max_hp))
        return pool
