import numpy as np
from itertools import combinations, permutations
from scipy.special import softmax
from scipy.stats import entropy
from copy import deepcopy

def true_entropy(team_generator, batch_predict, num_items:int, num_selections:int):

    P_A = np.zeros((num_items))
    past_probs = []

    for i in range(num_selections):
        sets = list(permutations(range(num_items), i+1))
        teams = [team_generator() for x in range(len(sets))]
        for j, s in enumerate(sets):
            for item in s:
                teams[j].mark(item)
        vals = batch_predict(teams)
        vals = softmax(vals.reshape(-1, num_items), axis=-1).reshape(-1)
        P = np.zeros(tuple([num_items for x in range(i + 1)]))

        for j, team in enumerate(teams):
            prefix_p = 1
            for k in range(len(team)):
                pp = past_probs[k - 1][tuple(team[z] for z in range(k))] if k > 0 else 1 # to help find the prefix
                #for z in range(k):
                #    pp = pp[team[z]]
                prefix_p *= pp
            #p_curse += vals[j]
            P[tuple(team[z] for z in range(len(team)))] += vals[j]
            P_A[team[-1]] += prefix_p * vals[j]
            print(P_A)
        past_probs.append(P) #somevariant of vals so that its easily indexible)
    print(P_A)
    entropy_loss = -entropy(P_A)
    return entropy_loss

def sample_based_entropy(team_generator, batch_predict, num_items:int, num_selections:int, num_samples:int):
    counts = np.zeros((num_items))
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
    print(P_A)
    entropy_loss = -entropy(P_A)
    return entropy_loss

def lower_bound_entropy(team_generator, batch_predict, num_items:int, num_selections:int):
    all_teams = [team_generator() for x in range(num_items)]
    for i in range(num_items):
        all_teams[i].mark(i) # just mark one element
    P_A = softmax(batch_predict(all_teams))
    entropy_loss = -entropy(P_A)
    print(P_A)
    return entropy_loss
