import argparse
import sys

from agent.Example_Competitor import ExampleCompetitor
from agent.Proposed_Competitor import ProposedCompetitor
from vgc.balance.meta import StandardMetaData
from vgc.balance.restriction import VGCDesignConstraints
from vgc.competition import CompetitorManager
from vgc.ecosystem.GameBalanceEcosystem import GameBalanceEcosystem
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

NUM_PKM = 5
def plot_rewards(rewards: list) -> None:
    import matplotlib.pyplot as plt
    print(rewards)
    plt.scatter(range(len(rewards)), rewards)
    plt.xlabel("Iterations")
    plt.ylabel("Reward")
    plt.title("Reward for Stage 1 per iteration")
    plt.xticks(range(len(rewards)))
    plt.show()


def main(args):
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
    meta_data = StandardMetaData()
    meta_data.set_moves_and_pkm(base_roster)
    gbe = GameBalanceEcosystem(competitor, surrogate_agent, constraints, base_roster, meta_data, debug=False)
    gbe.run(n_epochs=n_epochs, n_vgc_epochs=n_vgc_epochs, n_league_epochs=n_league_epochs)
    results.append((competitor.name, sum(gbe.rewards)))
    winner_name = ""
    max_score = 0.0

    plot_rewards(gbe.rewards)
    """
    for name, score in results:
        if score > max_score:
            winner_name = name
    print(winner_name + " wins the competition with score", max_score)
    for i in base_roster:
        print(i, i.pkm_id)

    check_dict = {}
    correct_count = 0
    change_id = -1
    for i in base_roster:
        if i.max_hp == 2:
            change_id = i.pkm_id
            for j in i.move_roster:
                check_dict[str(j)] = j.power
        break
    
    print(check_dict, correct_count, meta_data._moves[4*change_id])
    for i in range(len(meta_data._pkm)):
        if meta_data._pkm[i].pkm_id == change_id:
            for move in meta_data._moves[4 * i: 4 * i + 4]:
                print(move.power, move)

    for i in base_roster:
        for j in i.move_roster:
            if str(j) in check_dict:
                print(j.power, j)
                assert(j.power == check_dict[str(j)])
                correct_count += 1
    print(check_dict, correct_count, meta_data._moves[4*change_id])
    """

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_epochs', type=int, help='Number of updates to be done', default=1)
    parser.add_argument('--n_vgc_epochs', type=int, default=1)
    parser.add_argument('--n_league_epochs', type=int, default=1)
    parser.add_argument('--population_size', type=int, default=2)
    args = parser.parse_args()
    main(args)
