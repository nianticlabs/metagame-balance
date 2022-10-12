# Competition
DEFAULT_MATCH_N_BATTLES = 3

# Roster
DEFAULT_ROSTER_SIZE = 150
DEFAULT_MOVE_ROSTER_SIZE = 69
DEFAULT_N_MOVES_PKM = 4

# Teams
DEFAULT_TEAM_SIZE = 2
DEFAULT_PARTY_SIZE = DEFAULT_TEAM_SIZE - 1
MAX_TEAM_SIZE = 6

# Move power
MOVE_POWER_MIN = 0.
MOVE_POWER_MAX = 140.

# Move power point
MOVE_MAX_PP = 20
MOVE_MED_PP = MOVE_MAX_PP // 2

# Number actions
DEFAULT_PKM_N_MOVES = 4
DEFAULT_N_ACTIONS = DEFAULT_PKM_N_MOVES + DEFAULT_PARTY_SIZE

# Hit Points
MAX_HIT_POINTS = 240.
MIN_HIT_POINTS = 10.
BASE_HIT_POINTS = 120.

# Hazard damage
STATE_DAMAGE = MAX_HIT_POINTS / 8.
SPIKES_2 = MAX_HIT_POINTS / 6.
SPIKES_3 = MAX_HIT_POINTS / 4.

# Pkm type chart
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
    (1., .5, 1., 1., 1., 1., 2., .5, 1., 1., 1., 1., 1., 1., 2., 2., .5, 1.)  # FAIRY
)

TYPES = ['NORMAL', 'FIRE', 'WATER', 'ELECTRIC', 'GRASS', 'ICE', 'FIGHTING', 'POISON', 'GROUND', 'FLYING', 'PSYCHIC',
         'BUG', 'ROCK', 'GHOST', 'DRAGON', 'DARK', 'STEEL', 'FAIRY']

NUM_TYPES = len(TYPE_CHART_MULTIPLIER)

# OPT parameters
STATS_OPT_2_PER_MOVE = 3 + NUM_TYPES
STATS_OPT_2_PER_PKM = 1 + NUM_TYPES

STATS_OPT_1_PER_MOVE = 3
STATS_OPT_1_PER_PKM = 1

MAX_MOVE_POWER = 150
MAX_MOVE_ACC = 1.
MAX_MOVE_MAX_PP = 20
MAX_PKM_HP = 500


# Stage 2 STATE DIM
def get_state_size(team_size: int) -> int:
    return team_size * (STATS_OPT_2_PER_PKM + DEFAULT_N_MOVES_PKM * STATS_OPT_2_PER_MOVE)
