import argparse
import numpy as np
from agent.Example_Competitor import ExampleCompetitor
from agent.Proposed_Competitor import ProposedCompetitor
from agent.Seq_Softmax_Competitor import SeqSoftmaxCompetitor
from vgc.balance.meta import StandardMetaData
from vgc.balance.Winrate_Entropy_Meta import WinrateEntropyMetaData
from vgc.balance.restriction import VGCDesignConstraints
from vgc.competition import CompetitorManager
from vgc.ecosystem.GameBalanceEcosystem import GameBalanceEcosystem
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from Utility_Fn_Manager import UtilityFunctionManager
NUM_PKM = 30


def plot_rewards(loss: list, smoothing_over = 10) -> None:
    import matplotlib.pyplot as plt

    rewards = [-r for r in loss]
    conv_filter = np.ones((smoothing_over)) / smoothing_over
    smooth_rewards = np.convolve(conv_filter, rewards, 'valid')

    print(rewards)
    plt.plot(range(len(smooth_rewards)), smooth_rewards)
    plt.xlabel("Iterations")
    plt.ylabel("Reward")
    plt.title("Reward for Stage 1 per iteration")
    plt.show()


def main(args):
    """
    Main function: used to balance meta as well as learn the policy (TBI)
    This runs for `n_epochs' stage 1 optimization epochs 'n_vgc_epochs' stage 2 optimization epochs
    This also plots rewards per stage 1 iteration
    TODO Stage 2 plots log to files
    TODO Handle the noise in stage 1 plots (by smoonthing and plotting varience)
    """

    assert(args.population_size == 2) # Limit scope to two agents
    agent_names = ['agent', 'adversary']
    n_epochs = args.n_epochs
    n_vgc_epochs = args.n_vgc_epochs
    n_league_epochs = args.n_league_epochs
    population_size = args.population_size

    if args.roster_path == '':
        base_roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=NUM_PKM).gen_roster()
    else:
        import pickle
        base_roster = pickle.load(open(args.roster_path, 'rb'))
    """
    Code below is to create a an Roster with a OP pokmeon
    OP is defined as max health and max stats for one unique move to that pokemon
    TODO: use json instead of pickle
    """
    """
    base_roster = list(base_roster)
    from collections import defaultdict
    seen_moves = defaultdict(int)
    for pkm in base_roster:
        for move in pkm.move_roster:
            seen_moves[move] += 1

    for pkm in base_roster:
        for move in pkm.move_roster:
            if seen_moves[move] == 1:
                pkm.max_hp = 500
                move.power = 150
                move.acc = 100
                move.max_pp = 20
                break
        if pkm.max_hp == 500:
            break
    print(base_roster[0].max_hp)
    if base_roster[0].max_hp == 500:
        for move in base_roster[0].move_roster:
            print(move.name, move.power, move.acc, move.max_pp)
        import pickle
        pickle.dump(base_roster, open("roster_30_OP_1.pkl", 'wb'))
    import sys
    sys.exit(0)
    """
    """
    Code below is to generate roster pokmeons with same move set but different (random max hp)
    """
    """
    from copy import deepcopy
    import random
    pkm = list(RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=1).gen_roster())[0]
    base_roster = [deepcopy(pkm) for i in range(NUM_PKM)]
    for i in range(NUM_PKM):
        base_roster[i].pkm_id = i
        base_roster[i].max_hp = random.randint(100, 300)

    """

    utility_fn_manager = UtilityFunctionManager(delay_by = 10)
    surrogate_agent = [CompetitorManager(SeqSoftmaxCompetitor(agent_name, utility_fn_manager)) for agent_name in agent_names]
    constraints = VGCDesignConstraints(base_roster)
    for i in base_roster:
        print(i, i.pkm_id)
    results = []
    competitor = ProposedCompetitor(NUM_PKM)
    meta_data = WinrateEntropyMetaData()
    meta_data.set_moves_and_pkm(base_roster)
    gbe = GameBalanceEcosystem(competitor, surrogate_agent, constraints, base_roster, meta_data, debug=False)
    gbe.run(n_epochs=n_epochs, n_vgc_epochs=n_vgc_epochs, n_league_epochs=n_league_epochs)
    results.append((competitor.name, sum(gbe.rewards)))
    winner_name = ""
    max_score = 0.0

    if args.visualize:
        plot_rewards(gbe.rewards)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_epochs', type=int, help='Number of updates to be done', default=1)
    parser.add_argument('--n_vgc_epochs', type=int, default=1)
    parser.add_argument('--n_league_epochs', type=int, default=1)
    parser.add_argument('--population_size', type=int, default=2)
    parser.add_argument('--roster_path', type=str, default='')
    parser.add_argument('--visualize', type=bool, default=False)
    args = parser.parse_args()
    main(args)
