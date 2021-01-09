from Engine.Competition.CompetitionStructures import TreeChampionship, Competitor
from Engine.Competition.PkmRosterGenerator import StandardPkmPoolGenerator


N_COMPETITORS = 16


def main():
    pool_gen = StandardPkmPoolGenerator(10, 100)
    competitors = [Competitor(name='Player ' + str(i)) for i in range(N_COMPETITORS)]
    tree_championship = TreeChampionship(pool_gen, competitors, debug=True)
    tree_championship.run()


if __name__ == '__main__':
    main()
