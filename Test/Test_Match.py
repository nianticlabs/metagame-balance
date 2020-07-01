from Engine.Competition.CompetitionStructures import Competitor, Match
from Engine.PkmTeamGenerator import RandomGenerator
from Player.GUIBattleAgent import GUIBattleAgent
from Player.GUISelectorAgent import GUISelectorAgent
from Player.RandomBattleAgent import RandomBattleAgent
from Player.RandomSelectorAgent import RandomSelectorAgent


def main():
    rg = RandomGenerator()
    c0 = Competitor(rg.get_team(), GUIBattleAgent(), GUISelectorAgent())
    c1 = Competitor(rg.get_team(), RandomBattleAgent(), RandomSelectorAgent())
    m = Match(c0, c1)
    m.run()
    print(m.records())


if __name__ == '__main__':
    main()
