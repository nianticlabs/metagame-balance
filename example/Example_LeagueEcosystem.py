from framework.competition.Competitor import ExampleCompetitor
from framework.ecosystem import CompetitorManager
from framework.ecosystem.LeagueEcosystem import LeagueEcosystem
from framework.util.Recording import DataDistributionManager
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.generator.PkmTeamGenerators import RandomGeneratorRoster

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    ddm = DataDistributionManager()
    le = LeagueEcosystem(ddm=ddm, debug=True, render=True)
    for i in range(N_PLAYERS):
        e_agent = ExampleCompetitor("Player %d" % i)
        e_agent.team = RandomGeneratorRoster(roster).get_team()
        le.register(CompetitorManager(e_agent, roster))
    le.run(10)


if __name__ == '__main__':
    main()
