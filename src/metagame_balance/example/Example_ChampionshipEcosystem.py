from metagame_balance.agent.Example_Competitor import ExampleCompetitor
from metagame_balance.vgc.balance.meta import StandardMetaData
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    meta_data = StandardMetaData()
    meta_data.set_moves_and_pkm(roster)
    ce = ChampionshipEcosystem(roster, meta_data, debug=True)
    for i in range(N_PLAYERS):
        cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
        ce.register(cm)
    ce.run(n_epochs=10, n_league_epochs=10)


if __name__ == '__main__':
    main()
