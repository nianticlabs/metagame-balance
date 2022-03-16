import numpy as np

from vgc.datatypes.Constants import MAX_HIT_POINTS, MOVE_POWER_MIN, MOVE_POWER_MAX, BASE_HIT_POINTS
from vgc.util import softmax


def get_stats(evs):
    evs = softmax(evs) * MAX_HIT_POINTS * 4
    evs = np.clip(evs, a_min=MOVE_POWER_MIN, a_max=MOVE_POWER_MAX)
    evs[0] += BASE_HIT_POINTS
    return evs
