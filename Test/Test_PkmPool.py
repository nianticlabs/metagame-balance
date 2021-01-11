from Behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from Util.PkmRosterGenerators import StandardPkmRosterGenerator


def main():
    pool_gen = StandardPkmRosterGenerator(10, 100)
    pool = pool_gen.get_pool()
    for pt in pool:
        print(pt)
        print()

    a = RandomTeamBuilderPolicy()
    t = a.get_action(pool)
    print(t)


if __name__ == '__main__':
    main()
