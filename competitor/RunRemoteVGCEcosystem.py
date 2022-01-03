from multiprocessing.connection import Client

from framework.behaviour.Proxy import ProxyCompetitor
from framework.ecosystem.VGCEcosystem import VGCEcosystem
from framework.util.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.PkmTeamGenerators import RandomGeneratorRoster
from framework.util.Recording import DataDistributionManager

N_PLAYERS = 4


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    ddm = DataDistributionManager()
    le = VGCEcosystem(roster, debug=True, render=True, ddm=ddm)
    conns = []
    for i in range(N_PLAYERS):
        address = ('localhost', 5000 + i)
        conn = Client(address, authkey=f'Competitor {i}'.encode('utf-8'))
        conns.append(conn)
        e_agent = ProxyCompetitor(conn)
        e_agent.team = RandomGeneratorRoster(roster).get_team()
        le.register(e_agent)
    le.run(n_epochs=10, n_league_epochs=10)
    for conn in conns:
        conn.close()


if __name__ == '__main__':
    main()
