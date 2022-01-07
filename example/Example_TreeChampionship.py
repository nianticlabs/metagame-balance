from framework.competition.Competition import TreeChampionship
from framework.competition.Competitor import ExampleCompetitor
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.generator.PkmTeamGenerators import RandomGeneratorRoster

N_COMPETITORS = 16


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    team_gen = RandomGeneratorRoster(roster)
    competitors = [ExampleCompetitor('Player ' + str(i), team_gen.get_team()) for i in range(N_COMPETITORS)]
    championship = TreeChampionship(roster, debug=True)
    for competitor in competitors:
        championship.register(competitor)
    championship.new_tournament()
    championship.run()


if __name__ == '__main__':
    main()
