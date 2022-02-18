from example.Example_Competitor import ExampleCompetitor
from vgc.balance.meta import StandardMetaData
from vgc.competition import CompetitorManager
from vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    meta_data = StandardMetaData()
    ce = ChampionshipEcosystem(roster, meta_data, debug=True)
    for i in range(N_PLAYERS):
        cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
        ce.register(cm)
    ce.run(n_epochs=10, n_league_epochs=10)


if __name__ == '__main__':
    main()
