from metagame_balance.vgc.behaviour.BattlePolicies import RandomBattlePolicy
from metagame_balance.vgc.engine.PkmBattleEnv import PkmBattleEnv


def main():
    env = PkmBattleEnv(debug=True)
    env.reset()
    t = False
    a0 = RandomBattlePolicy()
    a1 = RandomBattlePolicy()
    ep = 0
    n_battles = 3
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
            env.render()
        t = False
    a0.close()


if __name__ == '__main__':
    main()
