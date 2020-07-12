from Agent.GUISelectorAgent import GUISelectorAgent
from Engine.PkmBattleEngine import PkmBattleEngine
from Engine.PkmTeamGenerator import RandomGenerator


def main():
    env = PkmBattleEngine(debug=True)
    env.set_team_generator(RandomGenerator())
    env.reset()
    v0, v1 = env.team_view
    a = GUISelectorAgent()
    print(a.get_action(v0))


if __name__ == '__main__':
    main()
