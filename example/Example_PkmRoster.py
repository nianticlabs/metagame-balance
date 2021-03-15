from framework.DataObjects import get_pkm_roster_view, MetaData
from framework.behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from framework.behaviour.TeamValuators import NullTeamValuator
from framework.util.PkmRosterGenerators import RandomPkmRosterGenerator


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    for pt in roster:
        print(pt)

    a = RandomTeamBuilderPolicy()
    t = a.get_action((MetaData(), None, get_pkm_roster_view(roster), NullTeamValuator.null_team_value))
    print(t)


if __name__ == '__main__':
    main()
