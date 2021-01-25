from Framework.Competition.CompetitionObjects import Competitor, TreeChampionship
from Util.PkmRosterGenerators import RandomPkmRosterGenerator

N_COMPETITORS = 16


def main():
    pool_gen = RandomPkmRosterGenerator(10, 100)
    competitors = [Competitor(name='Player ' + str(i)) for i in range(N_COMPETITORS)]
    tree_championship = TreeChampionship(pool_gen, competitors, debug=True)
    tree_championship.run()


if __name__ == '__main__':
    main()
