from competitor.example.Example import Example
from framework.ecosystem.VGCEcosystem import VGCEcosystem
from framework.util.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.PkmTeamGenerators import RandomGeneratorRoster
from framework.util.Recording import DataDistributionManager

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    ddm = DataDistributionManager()
    le = VGCEcosystem(roster, debug=True, render=True, ddm=ddm)
    for i in range(N_PLAYERS):
        e_agent = Example("Player %d" % i)
        e_agent.team = RandomGeneratorRoster(roster).get_team()
        le.register(e_agent)
    le.run(n_epochs=10, n_league_epochs=10)


if __name__ == '__main__':
    main()
