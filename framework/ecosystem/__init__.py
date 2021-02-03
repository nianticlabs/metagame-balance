from copy import deepcopy
from typing import List
from elo import INITIAL
from framework.DataObjects import PkmFullTeam
from framework.competition.CompetitionObjects import Competitor


class CompetitorManager:

    def __init__(self, c: Competitor):
        self.__c = c
        self.__teams: List[PkmFullTeam] = []
        self.__n_battles = 0
        self.__elo = INITIAL

    @property
    def competitor(self) -> Competitor:
        return self.__c

    def get_team(self, idx: int) -> PkmFullTeam:
        return self.__teams[idx]

    def add_team(self, team: PkmFullTeam):
        self.__teams.append(deepcopy(team))

    @property
    def n_teams(self) -> int:
        return len(self.__teams)

    def add_n_battles(self):
        self.__n_battles += 1

    @property
    def elo(self) -> float:
        return self.__elo

    @elo.setter
    def elo(self, elo):
        self.__elo = elo

    @property
    def n_battles(self) -> int:
        return self.__n_battles
