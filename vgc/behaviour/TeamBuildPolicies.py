import random
from typing import List, Tuple, Optional

from vgc.balance.meta import MetaData
from vgc.behaviour import TeamBuildPolicy
from vgc.datatypes.Constants import MAX_TEAM_SIZE, DEFAULT_PKM_N_MOVES
from vgc.datatypes.Objects import Pkm, PkmTemplate, PkmRosterView, PkmFullTeam, PkmTemplateView, PkmMove, MoveView


def move_template_from_view(mv: MoveView) -> PkmMove:
    pm = PkmMove()
    pm.power = mv.power
    pm.acc = mv.acc
    pm.pp = mv.pp
    pm.max_pp = mv.max_pp
    pm.type = mv.type
    pm.priority = mv.priority
    pm.prob = mv.prob
    pm.target = mv.target
    pm.recover = mv.recover
    pm.status = mv.status
    pm.stat = mv.stat
    pm.stage = mv.stage
    pm.stage = mv.stage
    pm.fixed_damage = mv.fixed_damage
    pm.weather = mv.weather
    pm.hazard = mv.hazard
    return pm


def pkm_template_from_view(ptv: PkmTemplateView) -> PkmTemplate:
    pmr = set()
    pmrv = ptv.get_move_roster_view()
    for i in range(pmrv.n_moves):
        pmr.add(move_template_from_view(pmrv.get_move_view(i)))
    return PkmTemplate(pmr, ptv.pkm_type, ptv.max_hp, ptv.pkm_id)


class RandomTeamBuildPolicy(TeamBuildPolicy):

    def close(self):
        pass

    def get_action(self, d: Tuple[MetaData, Optional[PkmFullTeam], PkmRosterView]) -> PkmFullTeam:
        r_view = d[2]
        pre_selection: List[PkmTemplate] = [pkm_template_from_view(r_view.get_pkm_template_view(i)) for i in
                                            random.sample(range(r_view.n_pkms), MAX_TEAM_SIZE)]
        team: List[Pkm] = []
        for pt in pre_selection:
            team.append(pt.gen_pkm(random.sample(range(len(pt.move_roster)), DEFAULT_PKM_N_MOVES)))
        return PkmFullTeam(team)


class IdleTeamBuildPolicy(TeamBuildPolicy):

    def close(self):
        pass

    def get_action(self, d: Tuple[MetaData, Optional[PkmFullTeam], PkmRosterView]) -> PkmFullTeam:
        return d[1]
