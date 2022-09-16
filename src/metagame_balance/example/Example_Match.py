from metagame_balance.agent.Example_Competitor import ExampleCompetitor
from metagame_balance.vgc.competition import CompetitorManager
from metagame_balance.vgc.competition import BattleMatch
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from metagame_balance.vgc.util.generator.PkmTeamGenerators import RandomTeamFromRoster


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    tg = RandomTeamFromRoster(roster)
    cm0 = CompetitorManager(ExampleCompetitor("Player 1"))
    cm0.team = tg.get_team()
    cm1 = CompetitorManager(ExampleCompetitor("Player 2"))
    cm1.team = tg.get_team()
    match = BattleMatch(cm0, cm1, debug=True)
    match.run()


if __name__ == '__main__':
    main()
