import logging
from copy import deepcopy
from itertools import permutations

import numpy as np
from scipy.special import softmax
from scipy.stats import entropy


def true_entropy(team_generator, batch_predict, num_items: int, num_selections: int):
    P_A = np.zeros((num_selections, num_items))  # basically P(A^i_j)
    past_probs = []

    for i in range(num_selections):
        # separately calculate P(A^i_j)

        # all possible permutations with team size upto i
        sets = list(permutations(range(num_items), i + 1))
        teams = [team_generator() for x in range(len(sets))]
        for j, s in enumerate(sets):
            for item in s:
                teams[j].mark(item)

        # put them together for a batch update
        vals = batch_predict(teams)
        # reshape them, so we can group by same prefix teams (so that p(last_element) sums to 1
        struct_vals = softmax(vals.reshape(-1, num_items - i), axis=1)
        vals = struct_vals.reshape(-1)

        # to add to past probabilities coz P(A^j| prod of A's < j)
        P = np.zeros((num_items,) * (i + 1))

        for j, team in enumerate(teams):
            prefix_p = 1
            for k in range(len(team)):
                pp = past_probs[k - 1][tuple(team[z] for z in range(k))] if k > 0 else 1  # to help find the prefix
                prefix_p *= pp
            P[tuple(team[z] for z in range(len(team)))] += vals[j]
            P_A[i, team[-1]] += prefix_p * vals[j]
            # print(team.pkms,  P_A[i, team[-1]], prefix_p, vals[j])
        past_probs.append(P)  # somevariant of vals so that its easily indexible)
    # print(P_A, np.sum(P_A, axis=1))
    # print((np.sum(P_A, axis=0)))
    # P_A  = np.sum(P_A, axis = 0)
    """
    P_X = np.zeros((num_items))

    for i in range(num_selections):
        accumulated_P = np.ones((num_items))
        for j in range(num_selections):
            if i != j:
                accumulated_P *= (np.ones((num_items)) - P_A[j])
        P_X += P_A[i] * accumulated_P
    """
    P_X = np.sum(P_A, axis=0) / num_selections
    entropy_loss = -entropy(P_X)
    logging.info("P_A=%s\tEntropy=%s\t", str(list(P_X)), str(entropy_loss))
    return entropy_loss


def sample_based_entropy(team_generator, batch_predict, num_items: int, num_selections: int, num_samples: int):
    counts = np.zeros(num_items)
    for i in range(num_samples):
        team = team_generator()
        for j in range(num_selections):
            tmp_teams = [deepcopy(team) for z in range(num_items)]
            items = [z for z in range(num_items)]
            for k, item in enumerate(items):
                tmp_teams[k].mark(item)
            vals = (batch_predict(tmp_teams))
            for k in range(len(team) - 1):
                vals[team[k]] = float("-inf")
            p = softmax(vals)
            selection = np.random.choice(range(num_items), p=p)
            team.mark(selection)
            counts[selection] += 1

    P_A = counts / sum(counts)
    entropy_loss = -entropy(P_A)
    logging.info("P_A=%s\tEntropy=%s\t", str(list(P_A)), str(entropy_loss))
    return entropy_loss


def lower_bound_entropy(team_generator, batch_predict, num_items: int, num_selections: int):
    all_teams = [team_generator() for x in range(num_items)]
    for i in range(num_items):
        all_teams[i].mark(i)  # just mark one element
    P_A = softmax(batch_predict(all_teams))
    entropy_loss = -entropy(P_A)
    logging.info("P_A=%s\tEntropy=%s\t", str(list(P_A)), str(entropy_loss))
    return entropy_loss
