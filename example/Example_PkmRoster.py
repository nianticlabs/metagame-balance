from vgc.balance.meta import MetaData
from vgc.behaviour.TeamBuildPolicies import RandomTeamBuildPolicy
from vgc.behaviour.TeamValuators import NullTeamValuator
from vgc.datatypes.Objects import get_pkm_roster_view
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    for pt in roster:
        print(pt)

    a = RandomTeamBuildPolicy()
    t = a.get_action((MetaData(), None, get_pkm_roster_view(roster), NullTeamValuator.null_team_value))
    print(t)


if __name__ == '__main__':
    main()
