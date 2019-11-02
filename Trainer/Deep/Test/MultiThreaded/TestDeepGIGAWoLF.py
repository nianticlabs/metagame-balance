from Environment.SimplePkmEnv import *
from Trainer.Deep.Learning.MultiThreaded.DeepGIGAWoLF import *
import tensorflow as tf

CONCURRENT_GAMES = 8
G_L_RATE = 1e-3
PI_L_RATE = 1 / 100  # 1 / 200
Y = .9
TAU = 25  # BATCH_SIZE
N_EPS = 200
N_STEPS = TAU
E_RATE = 0.1
N_PLAYERS = 2
ENV_NAME = 'SimplePkmEnv'
MODEL_PATH = '../../../../Model/Deep/DeepGIGAWoLF' + '_' + ENV_NAME


def main():
    print('train model SimplePkmEnv')
    env = SimplePkmEnv()
    trainer = DeepGIGAWoLF()
    trainer.train(env, G_L_RATE, CONCURRENT_GAMES, PI_L_RATE, Y, TAU, N_EPS, N_STEPS, E_RATE, N_PLAYERS, MODEL_PATH,
                  ENV_NAME)


if __name__ == "__main__":
    main()
