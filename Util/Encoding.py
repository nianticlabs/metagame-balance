from Framework.DataConstants import MAX_HIT_POINTS, MOVE_MAX_PP
from Framework.DataObjects import PkmMove, Pkm, PkmTeam
from Framework.DataTypes import N_TYPES, N_STATUS, N_STATS, N_STAGES, N_ENTRY_HAZARD, N_HAZARD_STAGES, N_WEATHER, \
    PkmStat, PkmType, PkmStatus, WeatherCondition, PkmEntryHazard


def one_hot(p, n):
    b = [0] * n
    b[p] = 1
    return b


def encode_move(e, move: PkmMove):
    e += [move.power / MAX_HIT_POINTS,
          move.acc,
          float(move.pp / MOVE_MAX_PP),
          move.priority,
          move.prob,
          move.target,
          move.recover / MAX_HIT_POINTS,
          move.stat.value,
          move.stage / 2,
          move.fixed_damage / MAX_HIT_POINTS]
    e += one_hot(move.type, N_TYPES)
    e += one_hot(move.status, N_STATUS)
    e += one_hot(move.weather, N_WEATHER)
    e += one_hot(move.hazard, N_ENTRY_HAZARD)


def decode_move(e) -> PkmMove:
    power = e[0] * MAX_HIT_POINTS
    acc = e[1]
    pp = int(e[2] * MOVE_MAX_PP)
    priority = e[3]
    prob = e[4]
    target = e[5]
    recover = e[6] * MAX_HIT_POINTS
    stat = PkmStat(e[7])
    stage = e[8] * 2
    fixed_damage = e[9] * MAX_HIT_POINTS
    _start = 10
    _end = _start + N_TYPES
    move_type = PkmType(e.index(1, _start, _end) - _start)
    _start = _end
    _end = _start + N_STATUS
    status = PkmStatus(e.index(1, _start, _end) - _start)
    _start = _end
    _end = _start + N_WEATHER
    weather = WeatherCondition(e.index(1, _start, _end) - _start)
    _start = _end
    _end = _start + N_ENTRY_HAZARD
    hazard = PkmEntryHazard(e.index(1, _start, _end) - _start)
    move = PkmMove(power=power, acc=acc, max_pp=pp, priority=priority, prob=prob, target=target, recover=recover,
                   stat=stat, stage=stage, fixed_damage=fixed_damage, move_type=move_type, status=status,
                   weather=weather, hazard=hazard)
    return move


def encode_pkm(e, pkm: Pkm):
    e += [pkm.hp / MAX_HIT_POINTS, pkm.n_turns_asleep / 5]
    e += one_hot(pkm.type, N_TYPES)
    e += one_hot(pkm.status, N_STATUS)
    # Pkm moves
    for move in pkm.moves:
        encode_move(e, move)


MOVE_ENCODE_LEN = 42


def decode_pkm(e):
    hp = e[0] * MAX_HIT_POINTS
    n_turns_asleep = int(e[1] * 5)
    _start = 2
    _end = _start + N_TYPES
    p_type = PkmType(e.index(1, _start, _end) - _start)
    _start = _end
    _end = _start + N_STATUS
    status = PkmStatus(e.index(1, _start, _end) - _start)
    _start = _end
    _end = _start + MOVE_ENCODE_LEN
    move0 = decode_move(e[_start:_end])
    _start = _end
    _end = _start + MOVE_ENCODE_LEN
    move1 = decode_move(e[_start:_end])
    _start = _end
    _end = _start + MOVE_ENCODE_LEN
    move2 = decode_move(e[_start:_end])
    _start = _end
    _end = _start + MOVE_ENCODE_LEN
    move3 = decode_move(e[_start:_end])
    pkm = Pkm(max_hp=hp, p_type=p_type, status=status, move0=move0, move1=move1, move2=move2, move3=move3)
    pkm.n_turns_asleep = n_turns_asleep
    return pkm


def encode_team(e, team: PkmTeam):
    e += [team.confused]
    for stat in range(N_STATS):
        e += [team.stage[stat] / N_STAGES]
    for hazard in range(N_ENTRY_HAZARD):
        e += one_hot(team.entry_hazard[hazard], N_HAZARD_STAGES)
    encode_pkm(e, team.active)
    for pkm in team.party:
        encode_pkm(e, pkm)


def decode_team(e):
    confused = e[0]


def encode_game_state(e, teams, weather):
    for team in teams:
        encode_team(e, team)
    e += one_hot(weather, N_WEATHER)
