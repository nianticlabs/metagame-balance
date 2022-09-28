from typing import Optional

from elo import INITIAL

from metagame_balance.vgc.competition import Competitor
from metagame_balance.vgc.datatypes.Constants import BASE_HIT_POINTS
from metagame_balance.vgc.datatypes.Objects import PkmRoster, Pkm, PkmTemplate, PkmFullTeam, PkmMove
from metagame_balance.vgc.datatypes.Types import PkmStatus, PkmEntryHazard, WeatherCondition


STANDARD_TOTAL_POINTS = 11


def get_move_points(move: PkmMove) -> int:
    points = 0
    points += max(int((move.power - 30.) / 30.) + ((move.power - 30.) % 30. > 0), 0)
    points += int(move.priority)
    points += int(move.recover > 0.)
    points += int(move.stage > 0.)
    points += int(move.status != PkmStatus.NONE)
    points += int(move.fixed_damage > 0.)
    points += int(move.weather != WeatherCondition.CLEAR)
    points += int(move.hazard != PkmEntryHazard.NONE)
    return points


def get_pkm_points(pkm: Pkm) -> int:
    points = 0
    points += int((pkm.hp - BASE_HIT_POINTS) / 30.) + ((pkm.hp - BASE_HIT_POINTS) % 30. > 0)
    for i in range(4):
        points += get_move_points(pkm.moves[i])
    return points


def legal_move_set(pkm: Pkm, template: PkmTemplate) -> bool:
    # there must be no repeated members
    for i in range(len(pkm.moves)):
        move = pkm.moves[i]
        for j in range(i + 1, len(pkm.moves)):
            if move == pkm.moves[j]:
                return False
    # all members must be instances of roster
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
    # there must be no repeated members
    for i in range(len(team.pkm_list)):
        pkm_id = team.pkm_list[i].pkm_id
        for j in range(i + 1, len(team.pkm_list)):
            if pkm_id == team.pkm_list[j].pkm_id:
                return False
    # all members must be instances of roster
    for pkm in team.pkm_list:
        for template in roster:
            if pkm.pkm_id == template.pkm_id:
                valid = pkm.type == template.type and 1.0 <= pkm.max_hp <= template.max_hp and legal_move_set(pkm,
                                                                                                              template)
                if not valid:
                    return False
    return True


class CompetitorManager:

    def __init__(self, c: Competitor):
        self.competitor = c
        self.team: Optional[PkmFullTeam] = None
        self.elo: float = INITIAL
