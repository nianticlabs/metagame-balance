from Behaviour.BattlePolicies import RandomBattlePolicy, SimpleBattlePolicy
from Util.PkmTeamGenerators import RandomGenerator
from Framework.Process.BattleEngine import PkmBattleEnv
from Util.Recording import GamePlayRecorder


def main():
    env = PkmBattleEnv(debug=True)
    env.set_team_generator(RandomGenerator())
    env.reset()
    t = False
    a0 = SimpleBattlePolicy()
    a1 = RandomBattlePolicy()
    ep = 0
    n_battles = 3
    r = GamePlayRecorder(name="test", c0="Player0", c1="Player1", t0=[env.teams[0].active] + env.teams[0].party,
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


if __name__ == '__main__':
    main()
