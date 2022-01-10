from multiprocessing.connection import Client

from framework.balance.meta import MetaData
from framework.competition import CompetitorManager
from framework.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from framework.network.ProxyCompetitor import ProxyCompetitor
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

N_PLAYERS = 4


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    meta_data = MetaData()
    ce = ChampionshipEcosystem(roster, meta_data, debug=True, render=True)
    conns = []
    for i in range(N_PLAYERS):
        address = ('localhost', 5000 + i)
        conn = Client(address, authkey=f'Competitor {i}'.encode('utf-8'))
        conns.append(conn)
        cm = CompetitorManager(ProxyCompetitor(conn))
        ce.register(cm)
    ce.run(n_epochs=10, n_league_epochs=10)
    for conn in conns:
        conn.close()


if __name__ == '__main__':
    main()
