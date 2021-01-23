
# Competition
DEFAULT_MATCH_N_BATTLES = 3

# Roster
DEFAULT_ROSTER_SIZE = 151
DEFAULT_MOVE_ROSTER_SIZE = 165
DEFAULT_N_MOVES_PKM = 10

# Teams
DEFAULT_TEAM_SIZE = 3
DEFAULT_PARTY_SIZE = DEFAULT_TEAM_SIZE - 1
MAX_TEAM_SIZE = 6

# Move power
MOVE_POWER_MIN = 40.
MOVE_POWER_MAX = 120.

# Move power point
MOVE_MAX_PP = 20
MOVE_MED_PP = MOVE_MAX_PP // 2

# Number actions
DEFAULT_PKM_N_MOVES = 4
DEFAULT_N_ACTIONS = DEFAULT_PKM_N_MOVES + DEFAULT_PARTY_SIZE

# Hit Points
MAX_HIT_POINTS = 240.
MIN_HIT_POINTS = 120.

# Hazard damage
STATE_DAMAGE = MAX_HIT_POINTS / 8.
SPIKES_2 = MAX_HIT_POINTS / 6.
SPIKES_3 = MAX_HIT_POINTS / 4.

# Stage
MAX_STAT_STAGE = 4
MIN_STAT_STAGE = -4

# Pkm Type Chart
TYPE_CHART_MULTIPLIER = (
    (1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., .5, .0, 1., 1., .5, 1.),  # NORMAL
    (1., .5, .5, 1., 2., 2., 1., 1., 1., 1., 1., 2., .5, 1., .5, 1., 2., 1.),  # FIRE
    (1., 2., .5, 1., .5, 1., 1., 1., 2., 1., 1., 1., 2., 1., .5, 1., 1., 1.),  # WATER
    (1., 1., 2., .5, .5, 1., 1., 1., 0., 2., 1., 1., 1., 1., .5, 1., 1., 1.),  # ELECTRIC
    (1., .5, 2., 1., .5, 1., 1., .5, 2., .5, 1., .5, 2., 1., .5, 1., .5, 1.),  # GRASS
    (1., .5, .5, 1., 2., .5, 1., 1., 2., 2., 1., 1., 1., 1., 2., 1., .5, 1.),  # ICE
    (2., 1., 1., 1., 1., 2., 1., .5, 1., .5, .5, .5, 2., 0., 1., 2., 2., .5),  # FIGHTING
    (1., 1., 1., 1., 2., 1., 1., .5, .5, 1., 1., 1., .5, .5, 1., 1., .0, 2.),  # POISON
    (1., 2., 1., 2., .5, 1., 1., 2., 1., 0., 1., .5, 2., 1., 1., 1., 2., 1.),  # GROUND
    (1., 1., 1., .5, 2., 1., 2., 1., 1., 1., 1., 2., .5, 1., 1., 1., .5, 1.),  # FLYING
    (1., 1., 1., 1., 1., 1., 2., 2., 1., 1., .5, 1., 1., 1., 1., 0., .5, 1.),  # PSYCHIC
    (1., .5, 1., 1., 2., 1., .5, .5, 1., .5, 2., 1., 1., .5, 1., 2., .5, .5),  # BUG
    (1., 2., 1., 1., 1., 2., .5, 1., .5, 2., 1., 2., 1., 1., 1., 1., .5, 1.),  # ROCK
    (0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 2., 1., 1., 2., 1., .5, 1., 1.),  # GHOST
    (1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 2., 1., .5, .0),  # DRAGON
    (1., 1., 1., 1., 1., 1., .5, 1., 1., 1., 2., 1., 1., 2., 1., .5, 1., .5),  # DARK
    (1., .5, .5, .5, 1., 2., 1., 1., 1., 1., 1., 1., 2., 1., 1., 1., .5, 2.),  # STEEL
    (1., .5, 1., 1., 1., 1., 2., .5, 1., 1., 1., 1., 1., 1., 2., 2., .5, 1.)   # FAIRY
)
