import random
from enum import IntEnum

from vgc.datatypes.Constants import TYPE_CHART_MULTIPLIER


class PkmType(IntEnum):
    NORMAL = 0
    FIRE = 1
    WATER = 2
    ELECTRIC = 3
    GRASS = 4
    ICE = 5
    FIGHT = 6
    POISON = 7
    GROUND = 8
    FLYING = 9
    PSYCHIC = 10
    BUG = 11
    ROCK = 12
    GHOST = 13
    DRAGON = 14
    DARK = 15
    STEEL = 16
    FAIRY = 17


N_TYPES = len(list(map(int, PkmType)))


def get_effective(t: PkmType) -> PkmType:
    """
    Get a random effective type relative to type t.

    :param t: pokemon type
    :return: a random type that is not very effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 1.]
    if not s:
        return PkmType(random.randrange(N_TYPES))
    return PkmType(random.choice(s))


def get_super_effective(t: PkmType) -> PkmType:
    """
    Get a random super effective type relative to type t.

    :param t: pokemon type
    :return: a random type that is super effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == 2.]
    if not s:
        print('Warning: Empty List!')
        return get_effective(t)
    return PkmType(random.choice(s))


def get_non_very_effective(t: PkmType) -> PkmType:
    """
    Get a random non very effective type relative to type t.

    :param t: pokemon type
    :return: a random type that is not very effective against pokemon type t
    """
    _t = [t_[t] for t_ in TYPE_CHART_MULTIPLIER]
    s = [index for index, value in enumerate(_t) if value == .5]
    if not s:
        return get_effective(t)
    return PkmType(random.choice(s))


# Battle Weather conditions
class WeatherCondition(IntEnum):
    CLEAR = 0
    SUNNY = 1
    RAIN = 2
    SANDSTORM = 3
    HAIL = 4


N_WEATHER = len(list(map(int, WeatherCondition)))


# Pokemon battle status
class PkmStatus(IntEnum):
    NONE = 0
    PARALYZED = 1
    POISONED = 2
    CONFUSED = 3
    SLEEP = 4
    FROZEN = 5
    BURNED = 6


N_STATUS = len(list(map(int, PkmStatus)))


# Pokemon battle stats
class PkmStat(IntEnum):
    ATTACK = 0
    DEFENSE = 1
    SPEED = 2


N_STATS = len(list(map(int, PkmStat)))
MAX_STAGE = 5
MIN_STAGE = -5
N_STAGES = MAX_STAGE - MIN_STAGE + 1


# Pokemon battle stats
class PkmEntryHazard(IntEnum):
    NONE = 0
    SPIKES = 1


N_ENTRY_HAZARD = len(list(map(int, PkmEntryHazard)))
N_HAZARD_STAGES = 3
