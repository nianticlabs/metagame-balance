from Engine.PkmBattleEngine import PkmBattleEngine
from Engine.PkmTeamGenerator import RandomGenerator
from Player.GUISelectionAgent import GUISelectionAgent


def main():
    env = PkmBattleEngine(debug=True)
    env.set_team_generator(RandomGenerator())
    s = env.reset()
    v0, v1 = env.team_view
    a = GUISelectionAgent()
    print(a.get_action(v0))


if __name__ == '__main__':
    main()
