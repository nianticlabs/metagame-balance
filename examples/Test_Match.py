from framework.behaviour import GUIBattlePolicy, RandomBattlePolicy
from framework.behaviour.SelectorPolicies import GUISelectorPolicy, RandomSelectorPolicy
from framework.competition.CompetitionObjects import Competitor, Match
from framework.util.PkmTeamGenerators import RandomGenerator


def main():
    rg = RandomGenerator()
    c0 = Competitor(rg.get_team(), GUIBattlePolicy(), GUISelectorPolicy())
    c1 = Competitor(rg.get_team(), RandomBattlePolicy(), RandomSelectorPolicy())
    m = Match(c0, c1, debug=True)
    m.run()


if __name__ == '__main__':
    main()
