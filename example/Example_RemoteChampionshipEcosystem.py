from multiprocessing.connection import Client

from vgc.balance.meta import StandardMetaData
from vgc.competition import CompetitorManager
from vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from vgc.network.ProxyCompetitor import ProxyCompetitor
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

N_PLAYERS = 4


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    meta_data = StandardMetaData()
    ce = ChampionshipEcosystem(roster, meta_data, debug=True)
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
