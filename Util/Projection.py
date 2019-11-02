import numpy as np


def projection(pi_in, th=0):
    """

    :param pi_in:
    :param th:
    :return:
    """
    pi = np.array(pi_in, dtype=np.float64)
    len_pi = len(pi_in)

    t = (1.0 - sum(pi)) / len(pi)
    pi += t

    while True:
        n = 0
        excess = 0
        for i in range(len_pi):
            if pi[i] < th:
                excess += th - pi[i]
                pi[i] = th
            elif pi[i] > th:
                n += 1

        # none negative? then done
        if excess == 0:
            break
        else:
            # otherwise decrement by equal steps
            for i in range(len_pi):
                if pi[i] > th:
                    pi[i] -= excess / n

    return pi

