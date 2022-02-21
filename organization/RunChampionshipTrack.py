import argparse
from multiprocessing.connection import Client

from vgc.balance.meta import StandardMetaData
from vgc.behaviour.TeamPredictors import NullTeamPredictor
from vgc.behaviour.TeamSelectionPolicies import FirstEditionTeamSelectionPolicy
from vgc.competition import CompetitorManager
from vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from vgc.network.ProxyCompetitor import ProxyCompetitor
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


def main(args):
    n_agents = args.n_agents
    n_epochs = args.n_epochs
    n_league_epochs = args.n_league_epochs
    base_port = args.base_port
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=100).gen_roster()
    meta_data = StandardMetaData()
    meta_data.set_moves_and_pkm(roster)
    conns = []
    ce = ChampionshipEcosystem(roster, meta_data, debug=True)  # , store_teams=True)
    for i in range(n_agents):
        address = ('localhost', base_port + i)
        conn = Client(address, authkey=f'Competitor {i}'.encode('utf-8'))
        conns.append(conn)
        competitor = ProxyCompetitor(conn)
        competitor.teamPredictor = NullTeamPredictor()
        competitor.teamSelectionPolicy = FirstEditionTeamSelectionPolicy()
        cm = CompetitorManager(competitor)
        ce.register(cm)
    ce.run(n_epochs=n_epochs, n_league_epochs=n_league_epochs)
    winner = ce.strongest()
    print(winner.competitor.name + " wins the tournament!")
    print(f"ELO {winner.elo}")
    for conn in conns:
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_agents', type=int, default=2)
    parser.add_argument('--n_epochs', type=int, default=10)
    parser.add_argument('--n_league_epochs', type=int, default=10)
    parser.add_argument('--base_port', type=int, default=5000)
    args = parser.parse_args()
    main(args)
