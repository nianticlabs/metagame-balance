from Behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from Util.PkmRosterGenerators import RandomPkmRosterGenerator


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
