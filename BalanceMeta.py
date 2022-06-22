import argparse
import sys

from agent.Example_Competitor import ExampleCompetitor
from agent.Proposed_Competitor import ProposedCompetitor
from vgc.balance.meta import StandardMetaData
from vgc.balance.Proposed_Meta import ProposedMetaData
from vgc.balance.restriction import VGCDesignConstraints
from vgc.competition import CompetitorManager
from vgc.ecosystem.GameBalanceEcosystem import GameBalanceEcosystem
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

NUM_PKM = 30
def plot_rewards(rewards: list) -> None:
    import matplotlib.pyplot as plt
    print(rewards)
    plt.scatter(range(len(rewards)), rewards)
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
    n_epochs = args.n_epochs
    n_vgc_epochs = args.n_vgc_epochs
    n_league_epochs = args.n_league_epochs
    population_size = args.population_size
    base_roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=NUM_PKM).gen_roster()
    surrogate_agent = [CompetitorManager(ExampleCompetitor()) for _ in range(population_size)]
    constraints = VGCDesignConstraints(base_roster)
    for i in base_roster:
        print(i, i.pkm_id)
    results = []
    competitor = ProposedCompetitor(NUM_PKM)
    meta_data = ProposedMetaData()
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
    parser.add_argument('--visualize', type=bool, default=False)
    args = parser.parse_args()
    main(args)
