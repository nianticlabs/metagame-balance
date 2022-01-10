from example.Example_Competitor import ExampleCompetitor
from framework.competition import CompetitorManager
from framework.competition.Competition import TreeChampionship
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

N_COMPETITORS = 16


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    competitors = [ExampleCompetitor('Player ' + str(i)) for i in range(N_COMPETITORS)]
    championship = TreeChampionship(roster, debug=True)
    for competitor in competitors:
        championship.register(CompetitorManager(competitor))
    championship.new_tournament()
    winner = championship.run()
    print(winner.competitor.name + " wins the tournament!")


if __name__ == '__main__':
    main()
