from Behaviour.SelectorPolicies import GUISelectorPolicy
from Framework.Competition.PkmTeamGenerator import RandomGenerator
from Framework.Process.BattleEngine import PkmBattleEnv


def main():
    env = PkmBattleEnv(debug=True)
    env.set_team_generator(RandomGenerator())
    env.reset()
    v0, v1 = env.team_view
    a = GUISelectorPolicy()
    print(a.get_action(v0))


if __name__ == '__main__':
    main()
