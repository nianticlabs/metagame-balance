from framework.DataObjects import get_pkm_roster_view
from framework.behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from framework.competition.CompetitionObjects import null_metadata, null_team_value
from framework.util.PkmRosterGenerators import RandomPkmRosterGenerator


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    for pt in roster:
        print(pt)
        print()

    a = RandomTeamBuilderPolicy()
    t = a.get_action((null_metadata, None, get_pkm_roster_view(roster), null_team_value))
    print(t)


if __name__ == '__main__':
    main()
