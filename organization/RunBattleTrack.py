import argparse
import time
from multiprocessing.connection import Client

from framework.competition.Competition import TreeChampionship
from framework.network.ProxyCompetitor import ProxyCompetitor
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


def main(args):
    n_agents = args.n_agents
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    conns = []
    championship = TreeChampionship(roster, name="Battle Competition " + time.strftime("%Y%m%d-%H%M%S"), debug=True)
    for i in range(n_agents):
        address = ('localhost', 5000 + i)
        conn = Client(address, authkey=f'Competitor {i}'.encode('utf-8'))
        conns.append(conn)
        championship.register(ProxyCompetitor(conn))
    championship.new_tournament()
    championship.run()
    for conn in conns:
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_agents', type=int, default=2)
    args = parser.parse_args()
    main(args)