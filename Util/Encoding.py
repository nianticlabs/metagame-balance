from Framework.DataConstants import MAX_HIT_POINTS, MOVE_MAX_PP
from Framework.DataObjects import PkmMove, Pkm, PkmTeam
from Framework.DataTypes import N_TYPES, N_STATUS, N_STATS, N_STAGES, N_ENTRY_HAZARD, N_HAZARD_STAGES, N_WEATHER


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
          move.stat,
          move.stage / 2,
          move.fixed_damage / MAX_HIT_POINTS]
    e += one_hot(move.type, N_TYPES)
    e += one_hot(move.status, N_STATUS)
    e += one_hot(move.weather, N_WEATHER)
    e += one_hot(N_ENTRY_HAZARD if move.hazard is None else move.hazard, N_ENTRY_HAZARD + 1)


def decode_move(e) -> PkmMove:
    move = PkmMove()

    return move


def encode_pkm(e, pkm: Pkm):
    e += [pkm.hp / MAX_HIT_POINTS]
    e += one_hot(pkm.type, N_TYPES)
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
    e += [team.confused]
    # stages
    for stat in range(N_STATS):
        e += [team.stage[stat] / N_STAGES]
    # entry hazards
    for hazard in range(N_ENTRY_HAZARD):
        e += one_hot(team.entry_hazard[hazard], N_HAZARD_STAGES)


def encode_game_state(e, teams, weather):
    # for each team
    for team in teams:
        encode_team(e, team)
    # weather
    e += one_hot(weather, N_WEATHER)
