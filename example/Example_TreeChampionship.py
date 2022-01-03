from framework.competition.Competition import TreeChampionship
from framework.competition.Competitor import ExampleCompetitor
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.generator.PkmTeamGenerators import RandomGeneratorRoster

N_COMPETITORS = 16


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    team_gen = RandomGeneratorRoster(roster)
    competitors = [ExampleCompetitor('Player ' + str(i), team_gen.get_team()) for i in range(N_COMPETITORS)]
    tree_championship = TreeChampionship(roster, competitors, debug=True)
    tree_championship.run()


if __name__ == '__main__':
    main()
