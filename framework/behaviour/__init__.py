from abc import ABC, abstractmethod
from typing import Any, Set, Union, List, Tuple

from framework.balance.meta import MetaData
from framework.datatypes.Objects import PkmRoster, PkmTeamPrediction, PkmFullTeam, TeamValue, GameStateView, \
    PkmFullTeamView, PkmRosterView


class Behaviour(ABC):

    @abstractmethod
    def get_action(self, s) -> Any:
        pass

    def requires_encode(self) -> bool:
        return False

    @abstractmethod
    def close(self):
        pass


class BattlePolicy(Behaviour):

    @abstractmethod
    def get_action(self, s: Union[List[float], GameStateView]) -> int:
        pass


class TeamSelectionPolicy(Behaviour):

    @abstractmethod
    def get_action(self, s: Tuple[PkmFullTeamView, PkmFullTeamView]) -> Set[int]:
        pass


class TeamBuildPolicy(Behaviour):

    @abstractmethod
    def get_action(self, s: Tuple[MetaData, PkmFullTeam, PkmRosterView, TeamValue]) -> PkmFullTeam:
        pass


class TeamPredictor(Behaviour):

    @abstractmethod
    def get_action(self, s: Tuple[PkmFullTeamView, MetaData]) -> PkmTeamPrediction:
        pass


class TeamValuator(Behaviour):

    @abstractmethod
    def get_action(self, s: Tuple[PkmFullTeam, MetaData]) -> TeamValue:
        pass


class BalancePolicy(Behaviour):

    @abstractmethod
    def get_action(self, s: Tuple[PkmRosterView, MetaData]) -> PkmRoster:
        pass
