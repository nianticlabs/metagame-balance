from framework.competition.CompetitionObjects import TreeChampionship, ExampleCompetitor
from framework.util.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.PkmTeamGenerators import RandomGeneratorRoster

N_COMPETITORS = 16


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    team_gen = RandomGeneratorRoster(roster)
    competitors = [ExampleCompetitor(team_gen.get_team(), name='Player ' + str(i)) for i in range(N_COMPETITORS)]
    tree_championship = TreeChampionship(roster, competitors, debug=True)
    tree_championship.run()


if __name__ == '__main__':
    main()
