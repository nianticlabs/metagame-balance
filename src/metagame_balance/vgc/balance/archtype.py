from copy import copy

from metagame_balance.vgc.datatypes.Constants import MAX_HIT_POINTS, MOVE_MAX_PP
from metagame_balance.vgc.datatypes.Objects import PkmMove, PkmTemplate, PkmFullTeam
from metagame_balance.vgc.datatypes.Types import WeatherCondition, PkmStatus, MAX_STAGE, PkmEntryHazard


def _remove_effects(move: PkmMove) -> PkmMove:
    move.target = 1
    move.recover = 0.0
    move.status = PkmStatus.NONE
    move.stat = 0
    move.stage = 0
    move.fixed_damage = False
    move.weather = WeatherCondition.CLEAR
    move.hazard = PkmEntryHazard.NONE
    return move


def std_move_dist(move0: PkmMove, move1: PkmMove) -> float:
    # attributes distances
    d_power = abs(move0.power - move1.power) / MAX_HIT_POINTS
    d_acc = abs(move0.acc - move1.acc)
    d_max_pp = float(abs(move0.max_pp - move1.max_pp)) / MOVE_MAX_PP
    d_type = float(move0.type != move1.type)
    d_priority = float(abs(move0.priority - move1.priority))
    # effects distance
    d_prob = abs(move0.prob - move1.prob)
    if move0.prob == 0.0:
        move0 = _remove_effects(copy(move0))
    if move1.prob == 0.0:
        move1 = _remove_effects(copy(move1))
    d_target = float(move0.target != move1.target)
    d_recover = abs(move0.recover - move1.recover) / MAX_HIT_POINTS
    d_status = float(move0.status != move1.status)
    d_stat = float(move0.stat != move1.stat)
    d_stage = float(abs(move0.stage - move1.stage)) / MAX_STAGE
    d_fixed_damage = float(move0.fixed_damage != move1.fixed_damage)
    d_weather = float(move0.weather != move1.weather)
    d_hazard = float(move0.hazard != move1.hazard)
    # compound distances
    d_base = d_power + 0.7 * d_acc + 0.1 * d_max_pp + d_type + 0.2 * d_priority
    d_effects = d_prob + d_target + d_recover + d_status + d_stat + d_stage + d_fixed_damage + d_weather + d_hazard
    # total distances
    return d_base + d_effects / 4.0


def std_pkm_dist(pkm0: PkmTemplate, pkm1: PkmTemplate, move_distance=std_move_dist) -> float:
    d_max_hp = abs(pkm0.max_hp - pkm1.max_hp) / MAX_HIT_POINTS
    d_type = float(pkm0.type != pkm1.type)
    d_moves = 0.0
    for move0, move1 in zip(pkm0.move_roster, pkm1.move_roster):
        d_moves += move_distance(move0, move1) / 5.25
    return d_max_hp + d_type + d_moves / 8.0


def std_team_dist(team0: PkmFullTeam, team1: PkmFullTeam, pokemon_distance=std_pkm_dist) -> float:
    d_pkms = 0.0
    t0 = team0.get_battle_team([0, 1, 2])
    t1 = team1.get_battle_team([0, 1, 2])
    for pkm0, pkm1 in zip([t0.active] + t0.party, [t1.active] + t1.party):
        tmp0 = PkmTemplate(set(pkm0.moves), pkm0.type, pkm0.max_hp, pkm0.pkm_id)
        tmp1 = PkmTemplate(set(pkm1.moves), pkm1.type, pkm1.max_hp, pkm1.pkm_id)
        d_pkms += pokemon_distance(tmp0, tmp1) / 5.25
    return d_pkms
