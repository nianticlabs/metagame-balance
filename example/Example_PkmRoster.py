from framework.behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from framework.competition.CompetitionObjects import null_metadata, null_team_value
from framework.util.PkmRosterGenerators import RandomPkmRosterGenerator


def main():
    roster = RandomPkmRosterGenerator(10, 100).gen_roster()
    for pt in roster:
        print(pt)
        print()

    a = RandomTeamBuilderPolicy()
    t = a.get_action((null_metadata, None, roster, null_team_value))
    print(t)


if __name__ == '__main__':
    main()
