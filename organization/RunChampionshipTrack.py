import argparse
from multiprocessing.connection import Client

from framework.balance.meta import MetaData
from framework.behaviour.TeamPredictors import NullTeamPredictor
from framework.behaviour.TeamSelectionPolicies import FirstEditionTeamSelectionPolicy
from framework.competition import CompetitorManager
from framework.competition.Competition import TreeChampionship
from framework.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from framework.network.ProxyCompetitor import ProxyCompetitor
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


def main(args):
    n_agents = args.n_agents
    n_epochs = args.n_epochs
    n_league_epochs = args.n_league_epochs
    base_port = args.base_port
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=100).gen_roster()
    meta_data = MetaData()
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
    # finals = TreeChampionship(roster, debug=True)
    # for cm in ce.league.competitors:
    #     finals.vgc_register(cm)
    # finals.new_tournament()
    # winner = finals.run()
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
