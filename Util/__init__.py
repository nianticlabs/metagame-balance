from abc import ABC
from typing import List, Tuple


class Recorder(ABC):

    def open(self):
        pass

    def close(self):
        pass

    def empty(self) -> bool:
        pass

    def clear(self):
        pass

    def full(self) -> bool:
        pass

    def save(self, append=True):
        pass

    def record(self, record: Tuple[List, int, int]):
        pass

    def starved(self) -> bool:
        pass

    def read(self) -> Tuple[List, int, int]:
        pass

    def load(self):
        pass
