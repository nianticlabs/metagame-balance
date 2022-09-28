from metagame_balance.vgc.balance.meta import StandardMetaData
from metagame_balance.vgc.behaviour.TeamBuildPolicies import RandomTeamBuildPolicy
from metagame_balance.vgc.datatypes.Objects import get_pkm_roster_view
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    for pt in roster:
        print(pt)

    a = RandomTeamBuildPolicy()
    t = a.get_action((StandardMetaData(), None, get_pkm_roster_view(roster)))
    print(t)


if __name__ == '__main__':
    main()
