from example.Example_Competitor import ExampleCompetitor
from framework.balance.meta import MetaData
from framework.competition import CompetitorManager
from framework.ecosystem.BattleEcosystem import BattleEcosystem
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.generator.PkmTeamGenerators import RandomTeamFromRoster

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    meta_data = MetaData()
    le = BattleEcosystem(meta_data, debug=True)
    for i in range(N_PLAYERS):
        cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
        cm.team = RandomTeamFromRoster(roster).get_team()
        le.register(cm)
    le.run(10)


if __name__ == '__main__':
    main()
