import codecs
import pickle
import time
from typing import Optional

from elo import INITIAL

from framework.competition import Competitor
from framework.datatypes.Objects import PkmRoster, Pkm, PkmTemplate, PkmFullTeam


def legal_move_set(pkm: Pkm, template: PkmTemplate):
    for move in pkm.moves:
        valid = False
        for roster_move in template.move_roster:
            valid = move == roster_move
            if valid:
                break
        if not valid:
            return False
    return True


def legal_team(team: PkmFullTeam, roster: PkmRoster) -> bool:
    for pkm in team.pkm_list:
        valid = False
        for template in roster:
            valid = pkm.type == template.type and pkm.max_hp == template.max_hp and legal_move_set(pkm, template)
            if valid:
                break
        if not valid:
            return False
    return True


class CompetitorManager:

    def __init__(self, c: Competitor):
        self.competitor = c
        self.team: Optional[PkmFullTeam] = None
        self.elo: float = INITIAL
        self.team_archive_path = time.strftime("%Y%m%d-%H%M%S") + '_' + self.competitor.name

    def get_archived_team(self, idx: int) -> PkmFullTeam:
        index = 0
        with open(self.team_archive_path, "r") as f:
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
        with open(self.team_archive_path, "a+") as f:
            f.writelines([codecs.encode(pickle.dumps(team), "base64").decode()])
