import argparse
from multiprocessing.connection import Client

from vgc.competition import CompetitorManager
from vgc.competition.Competition import TreeChampionship
from vgc.network.ProxyCompetitor import ProxyCompetitor
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from vgc.util.generator.PkmTeamGenerators import RandomTeamGenerator


def main(args):
    n_agents = args.n_agents
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=100).gen_roster()
    championship = TreeChampionship(roster, debug=True, gen=RandomTeamGenerator(2))
    conns = []
    for i in range(n_agents):
        address = ('localhost', 5000 + i)
        conn = Client(address, authkey=f'Competitor {i}'.encode('utf-8'))
        conns.append(conn)
        championship.register(CompetitorManager(ProxyCompetitor(conn)))
    championship.new_tournament()
    winner = championship.run()
    print(winner.competitor.name + " wins the tournament!")
    for conn in conns:
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_agents', type=int, default=2)
    args = parser.parse_args()
    main(args)
