import numpy as np
from itertools import combinations, permutations
from scipy.special import softmax
from scipy.stats import entropy
from copy import deepcopy

def true_entropy(team_generator, num_items:int, num_selections:int):

    P_A = np.zeros((num_items))
    past_probs = np.ones((num_items))

    for i in range(num_selections):
        sets = permutations(range(num_items), i+1)
        teams = [team_generator() for x in range(len(sets))]
        for j, s in enumerate(sets):
            for item in s:
                teams[j].mark(item)
        vals = batch_predict(teams)

        for j, team in enumerate(teams):
            P_A[teams[-1]] += vals[team[-1]]
        #do some caluclations to add to P_A
    print(all_sets)

def sample_based_entropy(team_generator, num_items:int, num_selections:int, num_samples:int):
    counts = np.zeros((num_items))
    for i in range(num_samples):
        team = team_generator()
        for j in range(num_selections):
            tmp_teams = [deepcopy(team) for z in range(num_selections)]
            items = [z for z in range(num_items)]
            for k, item in enumerate(items):
                tmp_teams[k].mark(item)
            vals = (batch_predict(tmp_teams))
            for t in team:
                vals[t] = float("-inf")
            p = softmax(vals)
            selection = np.random.choice(range(num_items), p)
            team.mark(selection)
            counts[selection] += 1

    P_A = softmax(counts)
    entropy_loss = -entropy(P_A)
    return entropy_loss



def lower_bound_entropy(team_generator, num_items:int, num_selections:int):
    all_teams = [team_generator() for x in len(num_items)]
    for i in range(num_items):
        all_teams[i].mark(i) # just mark one element
    P_A = softmax(batch_predict(all_teams))
    entropy_loss = -entropy(P_A)
    return entropy_loss
