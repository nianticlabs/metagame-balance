from copy import deepcopy
from typing import List
from elo import INITIAL
from framework.DataObjects import PkmFullTeam, PkmRoster
from framework.competition.CompetitionObjects import Competitor
from framework.module.TeamBuilding import TeamBuildingProcess


class CompetitorManager:

    def __init__(self, c: Competitor, roster: PkmRoster):
        self.__c = c
        self.__teams: List[PkmFullTeam] = []
        self.__n_battles = 0
        self.__elo = INITIAL
        self.tbp = TeamBuildingProcess(c, roster)

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

    def increment_n_battles(self):
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
