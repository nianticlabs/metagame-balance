from Behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from Engine.PkmPoolGenerator import StandardPkmPoolGenerator


def main():
    pool_gen = StandardPkmPoolGenerator(10, 100)
    pool = pool_gen.get_pool()
    for pt in pool:
        print(pt)
        print()

    a = RandomTeamBuilderPolicy()
    t = a.get_action(pool)
    print(t)


if __name__ == '__main__':
    main()
