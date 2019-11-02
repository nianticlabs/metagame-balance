from Environment.SimplePkmEnv import *
from Trainer.Deep.Learning.Distributed.DistributedDeepGIGAWoLF import *
import sys

G_L_RATE = 1e-4
PI_L_RATE = 1 / 100  # 1 / 200
Y = .9
TAU = 25  # BATCH_SIZE
N_EPS = 2000000
N_STEPS = TAU
E_RATE = 0.1
N_PLAYERS = 2
ENV_NAME = 'SimplePkmEnv(SETTING_HALF_DETERMINISTIC)'
MODEL_PATH = '../../../../Model/Deep/DistributedDeepGIGAWoLF' + '_' + ENV_NAME


def main():
    task_index = int(sys.argv[1])
    concurrent_games = int(sys.argv[2])
    url = "localhost"
    hosts = [url + ":" + str(2210 + i) for i in range(concurrent_games)]
    env = SimplePkmEnv(SETTING_HALF_DETERMINISTIC)
    trainer = DistributedDeepGIGAWoLF()
    print('train', task_index)
    trainer.train(env, G_L_RATE, concurrent_games, PI_L_RATE, Y, TAU, N_EPS, N_STEPS, E_RATE, N_PLAYERS, MODEL_PATH,
                  hosts, task_index)


if __name__ == '__main__':
    main()
