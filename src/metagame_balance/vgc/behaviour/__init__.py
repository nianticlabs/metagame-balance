from abc import ABC, abstractmethod
from typing import Any, Set, Union, List, Tuple

from vgc.balance import DeltaRoster
from vgc.balance.meta import MetaData
from vgc.balance.restriction import VGCDesignConstraints
from vgc.datatypes.Objects import PkmTeamPrediction, PkmFullTeam, GameStateView, PkmFullTeamView, PkmRosterView, \
    PkmTemplate


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
    def get_action(self, s: Tuple[MetaData, PkmFullTeam, PkmRosterView]) -> PkmFullTeam:
        pass


class TeamPredictor(Behaviour):

    @abstractmethod
    def get_action(self, s: Tuple[PkmFullTeamView, MetaData]) -> PkmTeamPrediction:
        pass


class BalancePolicy(Behaviour):

    @abstractmethod
    def get_action(self, s: Tuple[Set[PkmTemplate], MetaData, VGCDesignConstraints]) -> DeltaRoster:
        pass
