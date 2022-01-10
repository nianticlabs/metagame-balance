from example.Example_Competitor import ExampleCompetitor
from framework.balance.meta import MetaData
from framework.competition import CompetitorManager
from framework.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    meta_data = MetaData()
    ce = ChampionshipEcosystem(roster, meta_data, debug=True)
    for i in range(N_PLAYERS):
        cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
        ce.register(cm)
    ce.run(n_epochs=10, n_league_epochs=10)


if __name__ == '__main__':
    main()
