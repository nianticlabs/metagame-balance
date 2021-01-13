from Behaviour.BattlePolicies import GUIBattlePolicy, RandomBattlePolicy
from Behaviour.SelectorPolicies import GUISelectorPolicy, RandomSelectorPolicy
from Framework.Competition.CompetitionObjects import Competitor, Match
from Util.PkmTeamGenerators import RandomGenerator


def main():
    rg = RandomGenerator()
    c0 = Competitor(rg.get_team(), GUIBattlePolicy(), GUISelectorPolicy())
    c1 = Competitor(rg.get_team(), RandomBattlePolicy(), RandomSelectorPolicy())
    m = Match(c0, c1, debug=True)
    m.run()


if __name__ == '__main__':
    main()
