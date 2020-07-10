from Engine.Competition.CompetitionStructures import Competitor, Match
from Engine.PkmTeamGenerator import RandomGenerator
from Agent.GUIBattleAgent import GUIBattleAgent
from Agent.GUISelectorAgent import GUISelectorAgent
from Agent.RandomBattleAgent import RandomBattleAgent
from Agent.RandomSelectorAgent import RandomSelectorAgent


def main():
    rg = RandomGenerator()
    c0 = Competitor(rg.get_team(), GUIBattleAgent(), GUISelectorAgent())
    c1 = Competitor(rg.get_team(), RandomBattleAgent(), RandomSelectorAgent())
    m = Match(c0, c1, debug=True)
    m.run()


if __name__ == '__main__':
    main()
