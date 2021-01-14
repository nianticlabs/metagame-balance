from Behaviour.BattlePolicies import RandomBattlePolicy
from Behaviour.SelectorPolicies import GUISelectorPolicy, RandomSelectorPolicy
from Framework.Competition.PkmMatchEngine import PkmMatchEngine
from Util.Recorders import Recorder


def main():
    ba = RandomBattlePolicy()
    env = PkmMatchEngine(ba, ba, debug=True)
    t = False
    a0 = GUISelectorPolicy()
    a1 = RandomSelectorPolicy()
    r = Recorder(name="random_agent")
    ep = 0
    n_matches = 3
    while ep < n_matches:
        s = env.reset()
        v = env.team_selector.team_views
        ep += 1
        while not t:
            o0 = s[0] if a0.requires_encode() else v[0]
            o1 = s[1] if a1.requires_encode() else v[1]
            a = [a0.get_action(o0), a1.get_action(o1)]
            s, _, t, v = env.step(a)
            env.render()
        t = False
    r.save()
    a0.close()


if __name__ == '__main__':
    main()