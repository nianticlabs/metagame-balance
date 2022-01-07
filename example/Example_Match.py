from framework.competition.BattleMatch import BattleMatch
from framework.competition.Competitor import ExampleCompetitor
from framework.util.generator.PkmTeamGenerators import RandomGenerator


def main():
    rg = RandomGenerator()
    c0 = ExampleCompetitor("Player1")
    c1 = ExampleCompetitor("Player2")
    match = BattleMatch(c0, c1, rg.get_team(), rg.get_team(), debug=True)
    match.run()


if __name__ == '__main__':
    main()
