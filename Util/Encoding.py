from Framework.DataConstants import MAX_HIT_POINTS, MOVE_MAX_PP
from Framework.DataObjects import PkmMove, Pkm, PkmTeam
from Framework.DataTypes import N_TYPES, N_STATUS, N_STATS, N_STAGES, N_ENTRY_HAZARD, N_HAZARD_STAGES, N_WEATHER


def one_hot(p, n):
    b = [0] * n
    b[p] = 1
    return b


def encode_move(e, move: PkmMove):
    e += [move.power / MAX_HIT_POINTS]
    e += [move.acc]
    e += [float(move.pp / MOVE_MAX_PP)]
    e += one_hot(move.type, N_TYPES)
    e += [move.priority]
    e += [move.prob]
    e += [move.target]
    e += [move.recover / MAX_HIT_POINTS]
    e += [move.status]
    e += [move.stat]
    e += [move.stage / 2]
    e += [move.fixed_damage / MAX_HIT_POINTS]
    e += one_hot(move.weather, N_WEATHER)
    e += [move.hazard]


def encode_pkm(e, pkm: Pkm):
    e += one_hot(pkm.type, N_TYPES)
    e += [pkm.hp / MAX_HIT_POINTS]
    e += one_hot(pkm.status, N_STATUS)
    # Pkm moves
    for move in pkm.moves:
        encode_move(e, move)


def encode_team(e, team: PkmTeam):
    # active pkm
    encode_pkm(e, team.active)
    # party pkms
    for pkm in team.party:
        encode_pkm(e, pkm)
    # confusion status
    e += one_hot(team.confused, 2)
    # stages
    for stat in range(N_STATS):
        e += one_hot(team.stage[stat], N_STAGES)
    # entry hazards
    for hazard in range(N_ENTRY_HAZARD):
        e += one_hot(team.entry_hazard[hazard], N_HAZARD_STAGES)


def encode_game_state(e, teams, weather):
    # for each team
    for team in teams:
        encode_team(e, team)
    # weather
    e += one_hot(weather, N_WEATHER)
