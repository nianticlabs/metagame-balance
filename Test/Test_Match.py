from Engine.Competition.CompetitionStructures import Competitor, Match
from Engine.Competition.PkmTeamGenerator import RandomGenerator
from Behaviour.BattlePolicies import GUIBattlePolicy
from Behaviour.SelectorPolicies import GUISelectorPolicy
from Behaviour.RandomBattleAgent import RandomBattleAgent
from Behaviour.RandomSelectorAgent import RandomSelectorAgent


def main():
    rg = RandomGenerator()
    c0 = Competitor(rg.get_team(), GUIBattlePolicy(), GUISelectorPolicy())
    c1 = Competitor(rg.get_team(), RandomBattleAgent(), RandomSelectorAgent())
    m = Match(c0, c1, debug=True)
    m.run()


if __name__ == '__main__':
    main()
