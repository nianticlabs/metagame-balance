import argparse
from multiprocessing.connection import Client

from metagame_balance.vgc.balance.meta import StandardMetaData
from metagame_balance.vgc.behaviour.TeamPredictors import NullTeamPredictor
from metagame_balance.vgc.behaviour.TeamSelectionPolicies import FirstEditionTeamSelectionPolicy
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from metagame_balance.vgc.network.ProxyCompetitor import ProxyCompetitor
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


def main(args):
    n_agents = args.n_agents
    n_epochs = args.n_epochs
    n_league_epochs = args.n_league_epochs
    base_port = args.base_port
    roster = RandomPkmRosterGenerator().gen_roster()
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
