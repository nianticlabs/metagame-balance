from abc import ABC, abstractmethod
from typing import Any, List

from Engine.PkmBaseStructures import PkmTeam


class Agent(ABC):

    @abstractmethod
    def get_action(self, s) -> Any:
        pass

    @abstractmethod
    def requires_encode(self) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass


class BattleAgent(Agent):

    @abstractmethod
    def get_action(self, s) -> int:
        pass


class SelectorAgent(Agent):

    @abstractmethod
    def get_action(self, s) -> List[int]:
        pass


class BuilderAgent(Agent):

    @abstractmethod
    def get_action(self, s) -> PkmTeam:
        pass
