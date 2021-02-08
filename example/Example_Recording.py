import time
from framework.behaviour.BattlePolicies import SimpleBattlePolicy, RandomBattlePolicy
from framework.process.BattleEngine import PkmBattleEnv
from framework.util.Recording import GamePlayRecorder, Frame


def main():
    env = PkmBattleEnv(debug=True)
    env.reset()
    t = False
    a0 = SimpleBattlePolicy()
    a1 = RandomBattlePolicy()
    ep = 0
    n_battles = 3
    name = time.strftime("%Y%m%d-%H%M%S") + "_test"
    r = GamePlayRecorder(name=name, c0="Player0", c1="Player1", t0=[env.teams[0].active] + env.teams[0].party,
                         t1=[env.teams[1].active] + env.teams[1].party)
    r.init()
    while ep < n_battles:
        s = env.reset()
        v = env.game_state_view
        env.render()
        ep += 1
        while not t:
            o0 = s[0] if a0.requires_encode() else v[0]
            o1 = s[1] if a1.requires_encode() else v[1]
            a = [a0.get_action(o0), a1.get_action(o1)]
            s, _, t, v = env.step(a)
            r.record((s[0], s[1], a[0], a[1], t))
            env.render()
        t = False
    a0.close()
    r.save()

    # test loading
    r = GamePlayRecorder(name=name)
    r.open()

    frame: Frame = r.read()
    print(frame)
    while len(frame[0]) != 0:
        frame = r.read()
        print(frame)


if __name__ == '__main__':
    main()
