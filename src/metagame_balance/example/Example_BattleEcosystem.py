from metagame_balance.agent.Example_Competitor import ExampleCompetitor
from metagame_balance.vgc.balance.meta import StandardMetaData
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.ecosystem.BattleEcosystem import BattleEcosystem
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from metagame_balance.vgc.util.generator.PkmTeamGenerators import RandomTeamFromRoster

N_PLAYERS = 16


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    meta_data = StandardMetaData()
    le = BattleEcosystem(meta_data, debug=True)
    for i in range(N_PLAYERS):
        cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
        cm.team = RandomTeamFromRoster(roster).get_team()
        le.register(cm)
    le.run(10)


if __name__ == '__main__':
    main()
