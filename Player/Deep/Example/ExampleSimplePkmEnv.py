from Environment.SimplePkmEnv import *
from Player.Deep.DeepMixedAgent import *
# from Player.HumanAgent import *
from Player.RandomAgent import *


def main():
    env = SimplePkmEnv(debug=True)
    # p0 = HumanAgent(env.action_space.n, '1: Move 1, 2: Move 2, 3: Move 3, 4: Move 4, 5: Switch')
    p0 = RandomAgent(env.action_space.n)
    p1 = DeepMixedAgent(env.action_space.n,
                        '../../../Model/Deep/DistributedDeepGIGAWoLF_SimplePkmEnv(SETTING_HALF_DETERMINISTIC)')
    n_games = 1000
    s = env.reset()
    a = [None, None]
    t_r = [0, 0]
    # v = [0, 0]
    for i in range(n_games):
        # print('New Battle\n##########')
        # env.render()
        ep_reward = [0, 0]
        t = False
        while not t:
            a[0] = p0.get_action(s[0])
            a[1] = p1.get_action(s[1])
            _, r, t, _ = env.step(tuple(a))
            # env.render('player')
            # env.render()
            ep_reward = [ep_reward[0] + r[0], ep_reward[1] + r[1]]
        t_r = [t_r[0] + ep_reward[0], t_r[1] + ep_reward[1]]
        # print('Results:')
        if ep_reward[0] > ep_reward[1]:
            # print('Trainer 0 wins')
            # v[0] += 1
            pass
        elif ep_reward[0] == ep_reward[1]:
            # print('Trainer 0 and Trainer 1 draws')
            pass
        else:
            # print('Trainer 1 wins')
            # v[1] += 1
            pass
        # print()
        s = env.reset()
    # print('Trainer 0 win rate', v[0] / n_games)
    # print('Trainer 1 win rate', v[1] / n_games)
    print('Trainer 0 average reward', t_r[0] / (n_games * 4))
    print('Trainer 1 average reward', t_r[1] / (n_games * 4))


if __name__ == "__main__":
    main()
