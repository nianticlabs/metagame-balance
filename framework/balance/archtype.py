from copy import copy

from framework.datatypes.Constants import MAX_HIT_POINTS, MOVE_MAX_PP
from framework.datatypes.Objects import PkmMove
from framework.datatypes.Types import WeatherCondition, PkmStatus, MAX_STAGE, PkmEntryHazard


class TeamArchtype:
    pass


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


def move_distance(move0: PkmMove, move1: PkmMove) -> float:
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
    return d_base + 1 / 4 * d_effects
