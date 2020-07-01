from abc import ABC, abstractmethod
from typing import Any, List


class Agent(ABC):

    @abstractmethod
    def get_action(self, s) -> Any:
        pass

    @abstractmethod
    def close(self):
        pass


class BattleAgent(Agent):

    @abstractmethod
    def get_action(self, s) -> int:
        pass

    @abstractmethod
    def close(self):
        pass


class SelectionAgent(Agent):

    @abstractmethod
    def get_action(self, s) -> List[int]:
        pass

    @abstractmethod
    def close(self):
        pass
