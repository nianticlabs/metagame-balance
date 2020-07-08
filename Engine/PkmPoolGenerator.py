from abc import ABC, abstractmethod

from Engine.PkmBaseStructures import PkmPool, PkmMovePool
from Engine.PkmStandardMoves import STANDARD_MOVE_POOL


class PkmPoolGenerator(ABC):

    @abstractmethod
    def get_pool(self) -> PkmPool:
        pass


class StandardPkmPoolGenerator(PkmPoolGenerator):

    def __init__(self):
        self.move_pool: PkmMovePool = STANDARD_MOVE_POOL

    def get_pool(self) -> PkmPool:
        pass
