from vgc.balance.meta import StandardMetaData
from vgc.behaviour.TeamBuildPolicies import RandomTeamBuildPolicy
from vgc.datatypes.Objects import get_pkm_roster_view
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    for pt in roster:
        print(pt)

    a = RandomTeamBuildPolicy()
    t = a.get_action((StandardMetaData(), None, get_pkm_roster_view(roster)))
    print(t)


if __name__ == '__main__':
    main()
