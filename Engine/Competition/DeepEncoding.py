from Engine.PkmBaseStructures import N_STATUS, N_TYPES
from Engine.PkmConstants import HIT_POINTS


def one_hot(p, n):
    b = [0] * n
    b[p] = 1
    return b


def encode(s):
    """
    Encode Game state.

    :param s: game state
    :return: encoded game state in one hot vector
    """
    e = []
    for i in range(0, 21):
        if (i + 1) % 3 == 0:
            e += one_hot(s[i], N_STATUS)
        if ((i + 2) % 3) == 0:
            e += [(s[i] / HIT_POINTS)]
        else:
            e += one_hot(s[i], N_TYPES)
    for i in range(21, 29):
        if i % 2 == 0:
            e += [(s[i] / HIT_POINTS)]
        else:
            e += one_hot(s[i], N_TYPES)
    for i in range(29, 35):
        e += one_hot(s[i], N_TYPES)
    e += one_hot(s[35], 2)
    e += one_hot(s[36], 2)
    e += one_hot(s[37], 5)
    e += one_hot(s[38], 5)
    e += one_hot(s[39], 2)
    e += one_hot(s[40], 2)
    e += one_hot(s[41], 5)
    return e