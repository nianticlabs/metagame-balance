from typing import List

from Util.Projection import projection
import numpy as np


def wpl(n_actions: int, pi_l_rate: float, min_e_rate: float, q_t: List[float], pi_t: List[float]):
    # compute target policy
    for _a in range(n_actions):
        delta = 0  # derivative
        # compute difference between this reward and average reward
        for __a in range(n_actions):
            delta += q_t[_a] - q_t[__a]
            delta /= n_actions - 1
        # scale to sort of normalize the effect of a policy
        if delta > 0:
            # when we are favoring the best action, we take a lower delta_policy, so that we move slowly
            delta_policy = 1 - pi_t[_a]
        else:
            # when we are favoring the worst action, we take a higher delta_policy, so that we move quickly
            delta_policy = pi_t[_a]
        pi_t[_a] += pi_l_rate * delta * delta_policy
    # project policy back into valid policy space
    return projection(pi_t, min_e_rate)


def giga_wolf(n_actions: int, pi_l_rate: float, min_e_rate: float, q_t: List[float], pi_t: List[float],
              pi_slow_t: List[float]):
    # compute target policy
    avg_pi = [0] * n_actions  # average policy
    for a in range(n_actions):
        avg_pi[a] = pi_t[a] + pi_l_rate * q_t[a]
    # project this strategy
    avg_pi = projection(avg_pi, 0)
    # Update the agent's 'z' distribution, using the step size and 'possible' rewards
    z = [0] * n_actions
    for a in range(n_actions):
        z[a] = pi_slow_t[a] + pi_l_rate * q_t[a] / 3
    # project this strategy
    z = projection(z, min_e_rate)
    # Calculate delta using sum of squared differences
    num = np.sqrt(sum((np.array(z) - np.array(pi_slow_t)) ** 2))
    den = np.sqrt(sum((np.array(z) - np.array(avg_pi)) ** 2))
    # delta learning rate
    if den == 0:
        d_l_rate = 1
    else:
        d_l_rate = min(1, num / den)
    # do an update of the agent's strategy
    for a in range(n_actions):
        pi_slow_t[a] = z[a]
        pi_t[a] = avg_pi[a] + d_l_rate * (z[a] - avg_pi[a])
