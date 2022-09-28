import argparse
from multiprocessing.connection import Client

from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.competition.Competition import TreeChampionship
from metagame_balance.vgc.network.ProxyCompetitor import ProxyCompetitor
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from metagame_balance.vgc.util.generator.PkmTeamGenerators import RandomTeamGenerator


def main(args):
    n_agents = args.n_agents
    roster = RandomPkmRosterGenerator().gen_roster()
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
