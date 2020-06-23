from Engine.PkmBattleEngine import PkmBattleEngine
from Player.HeuristicReactiveAgent import HeuristicReactiveAgent
from Player.RandomAgent import RandomAgent


def main():
    env = PkmBattleEngine(debug=True)
    s = env.reset()
    env.render()
    t = False
    a0 = RandomAgent()
    a1 = RandomAgent()
    while not t:
        s, _, t, _ = env.step([a0.get_action(s[0]), a1.get_action(s[1])])
        env.render()


if __name__ == '__main__':
    main()
