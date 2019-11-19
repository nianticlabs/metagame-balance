from Environment.SimplePkmEnv import *
from random import randrange


def main():
    for i in range(100):
        t = randrange(18)
        print(TYPE_TO_STR[get_super_effective_move(t)], 'type is super effective against type', TYPE_TO_STR[t])
    print()
    for i in range(100):
        t = randrange(18)
        print(TYPE_TO_STR[get_normal_effective_move(t)], 'type is effective against type', TYPE_TO_STR[t])
    print()
    for i in range(100):
        t = randrange(18)
        print(TYPE_TO_STR[get_non_very_effective_move(t)], 'type is non very effective against type', TYPE_TO_STR[t])


if __name__ == '__main__':
    main()
