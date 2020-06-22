from abc import ABC, abstractmethod

from Engine.PkmBattleEnv import Pkm


class PkmBattleBaseCompetition(ABC):

    @abstractmethod
    def active_pkm(self, t_id: int) -> Pkm:
        pass

    @abstractmethod
    def party_pkm(self, t_id: int) -> Pkm:
        pass

    @abstractmethod
    def weather(self, t_id: int):
        pass

    @abstractmethod
    def stage(self, t_id: int, stat):
        pass

    @abstractmethod
    def stage_hazard(self, t_id: int, hazard):
        pass

    @abstractmethod
    def confused(self, t_id: int):
        pass

    @abstractmethod
    def status(self, pkm: Pkm):
        pass
