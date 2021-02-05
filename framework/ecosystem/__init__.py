import codecs
import pickle
from datetime import datetime

from elo import INITIAL
from framework.DataObjects import PkmFullTeam, PkmRoster
from framework.competition.CompetitionObjects import Competitor
from framework.module.TeamBuilding import TeamBuildingProcess


class CompetitorManager:

    def __init__(self, c: Competitor, roster: PkmRoster):
        self.__c = c
        self.__path = str(datetime.now()) + '_' + self.__c.name
        self.__n_teams = 0
        self.__n_battles = 0
        self.__elo = INITIAL
        self.tbp = TeamBuildingProcess(c, roster)

    @property
    def competitor(self) -> Competitor:
        return self.__c

    def get_team(self, idx: int) -> PkmFullTeam:
        index = 0
        with open(self.__path, "r") as f:
            while index < idx:
                line = f.readline()
                if not line:
                    return PkmFullTeam()
                index += 1
            line = f.readline()
            if not line:
                return PkmFullTeam()
            return pickle.loads(codecs.decode(line.encode(), "base64"))

    def record_team(self, team: PkmFullTeam):
        with open(self.__path, "a+") as f:
            f.writelines([codecs.encode(pickle.dumps(self.__c.team), "base64").decode()])
        self.__n_teams += 1

    @property
    def n_teams(self) -> int:
        return self.__n_teams

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
