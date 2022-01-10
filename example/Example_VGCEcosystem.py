from framework.balance.meta import MetaData
from framework.competition.Competitor import ExampleCompetitor
from framework.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.generator.PkmTeamGenerators import RandomGeneratorRoster

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    meta_data = MetaData()
    le = ChampionshipEcosystem(roster, meta_data, debug=True, render=True)
    for i in range(N_PLAYERS):
        e_agent = ExampleCompetitor("Player %d" % i)
        e_agent.team = RandomGeneratorRoster(roster).get_team()
        le.register(e_agent)
    le.run(n_epochs=10, n_league_epochs=10)


if __name__ == '__main__':
    main()
