from typing import List
from framework.DataConstants import DEFAULT_MATCH_N_BATTLES
from framework.DataObjects import PkmRoster
from framework.competition.CompetitionObjects import Competitor
from framework.ecosystem.LeagueEcosystem import LeagueEcosystem
from framework.module.TeamBuilding import TeamBuildingProcess
from framework.util.Recording import GamePlayRecorder


class VGCEcosystem:

    def __init__(self, roster: PkmRoster, debug=False, render=True, n_battles=DEFAULT_MATCH_N_BATTLES,
                 rec: GamePlayRecorder = None):
        self.__roster = roster
        self.__competitors: List[Competitor] = []
        self.__league: LeagueEcosystem = LeagueEcosystem(debug, render, n_battles, rec)

    def register(self, c: Competitor):
        if c not in self.__competitors:
            tbp = TeamBuildingProcess(c, self.__roster)
            tbp.run()
            c.team = tbp.output()
            self.__competitors.append(c)
