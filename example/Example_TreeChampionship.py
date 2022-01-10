from example.Example_Competitor import ExampleCompetitor
from framework.competition.Competition import TreeChampionship
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

N_COMPETITORS = 16


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    competitors = [ExampleCompetitor('Player ' + str(i)) for i in range(N_COMPETITORS)]
    championship = TreeChampionship(roster, debug=True)
    for competitor in competitors:
        championship.register(competitor)
    championship.new_tournament()
    championship.run()


if __name__ == '__main__':
    main()
