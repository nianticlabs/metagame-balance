from Engine.PkmMatchEngine import PkmMatchEngine
from Player.GUISelectorAgent import GUISelectorAgent
from Player.RandomBattleAgent import RandomBattleAgent
from Player.RandomSelectorAgent import RandomSelectorAgent
from Util.Recorder import Recorder


def main():
    ba = RandomBattleAgent()
    env = PkmMatchEngine(ba, ba, debug=True)
    t = False
    a0 = GUISelectorAgent()
    a1 = RandomSelectorAgent()
    r = Recorder(name="random_agent")
    ep = 0
    n_matches = 3
    while ep < n_matches:
        s = env.reset()
        ep += 1
        while not t:
            a = [a0.get_action(s[0]), a1.get_action(s[1])]
            s, _, t, v = env.step(a)
            env.render()
        t = False
    r.save()
    a0.close()


if __name__ == '__main__':
    main()
