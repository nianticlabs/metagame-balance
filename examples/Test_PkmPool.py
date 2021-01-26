from framework.behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from framework.util import RandomPkmRosterGenerator


def main():
    pool_gen = RandomPkmRosterGenerator(10, 100)
    pool = pool_gen.gen_roster()
    for pt in pool:
        print(pt)
        print()

    a = RandomTeamBuilderPolicy()
    t = a.get_action(pool)
    print(t)


if __name__ == '__main__':
    main()
