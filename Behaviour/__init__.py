from abc import ABC, abstractmethod
from typing import Any, List
from Framework.DataObjects import PkmTeam, PkmRoster


class Behaviour(ABC):

    @abstractmethod
    def get_action(self, s) -> Any:
        pass

    @abstractmethod
    def requires_encode(self) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass


class BattlePolicy(Behaviour):

    @abstractmethod
    def get_action(self, s) -> int:
        pass


class SelectorPolicy(Behaviour):

    @abstractmethod
    def get_action(self, s) -> List[int]:
        pass


class TeamBuilderPolicy(Behaviour):

    @abstractmethod
    def get_action(self, s) -> PkmTeam:
        pass


class TeamHyphotesizer(Behaviour):

    @abstractmethod
    def get_action(self, s) -> PkmTeam:
        pass


class DataAggregator(Behaviour):

    @abstractmethod
    def get_action(self, s) -> Any:
        pass


class TeamValuator(Behaviour):

    @abstractmethod
    def get_action(self, s) -> Any:
        pass


class BalancePolicy(Behaviour):

    @abstractmethod
    def get_action(self, s) -> PkmRoster:
        pass
