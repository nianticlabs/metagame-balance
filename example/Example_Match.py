from example.Example_Competitor import ExampleCompetitor
from vgc.competition import CompetitorManager
from vgc.competition.BattleMatch import BattleMatch
from vgc.util.generator.PkmTeamGenerators import RandomTeamGenerator


def main():
    rg = RandomTeamGenerator()
    cm0 = CompetitorManager(ExampleCompetitor("Player 1"))
    cm0.team = rg.get_team()
    cm1 = CompetitorManager(ExampleCompetitor("Player 2"))
    cm1.team = rg.get_team()
    match = BattleMatch(cm0, cm1, debug=True)
    match.run()


if __name__ == '__main__':
    main()
