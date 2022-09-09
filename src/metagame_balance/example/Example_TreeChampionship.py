from src.metagame_balance.agent.Example_Competitor import ExampleCompetitor
from src.metagame_balance.vgc.competition import CompetitorManager
from src.metagame_balance.vgc.competition import TreeChampionship
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

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
