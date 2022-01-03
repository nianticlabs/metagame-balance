from framework.competition.Competition import Match
from framework.competition.Competitor import GUIExampleCompetitor, ExampleCompetitor
from framework.util.generator.PkmTeamGenerators import RandomGenerator


def main():
    rg = RandomGenerator()
    c0 = GUIExampleCompetitor(rg.get_team(), "Player0")
    c1 = ExampleCompetitor("Player1", rg.get_team())
    m = Match(c0, c1, debug=True)
    m.run()


if __name__ == '__main__':
    main()
