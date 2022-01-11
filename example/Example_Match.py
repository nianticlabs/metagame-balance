from example.Example_Competitor import ExampleCompetitor
from framework.competition import CompetitorManager
from framework.competition.BattleMatch import BattleMatch
from framework.util.generator.PkmTeamGenerators import RandomTeamGenerator


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
