from Environment.SimplePkmEnv import *
from Player.Deep.DeepMixedAgent import *
from Player.HumanAgent import *


def main():
    env = SimplePkmEnv()
    p0 = HumanAgent(env.action_space.n, '1: Move 1, 2: Move 2, 3: Move 3, 4: Move 4, 5: Switch')
    p1 = DeepMixedAgent(env.action_space.n, '../../../Model/Deep/DistributedDeepGIGAWoLF_SimplePkmEnv')
    n_games = 10
    s = env.reset()
    a = [None, None]
    for i in range(n_games):
        print('New Battle\n##########')
        env.render()
        ep_reward = [0, 0]
        t = False
        while not t:
            a[0] = p0.get_action(s[0])
            a[1] = p1.get_action(s[1])
            _, r, t, _ = env.step(tuple(a))
            env.render('player')
            ep_reward = [ep_reward[0] + r[0], ep_reward[1] + r[1]]
        print('Results:')
        if ep_reward[0] > ep_reward[1]:
            print('Trainer 0 wins')
        elif ep_reward[0] == ep_reward[1]:
            print('Trainer 0 and Trainer 1 draws')
        else:
            print('Trainer 1 wins')
        print()
        s = env.reset()


if __name__ == "__main__":
    main()
