from framework.behaviour.TeamSelectionPolicies import GUITeamSelectionPolicy
from framework.datatypes.Objects import get_full_team_view
from framework.util.generator.PkmTeamGenerators import RandomTeamGenerator


def main():
    a = GUITeamSelectionPolicy()
    team_gen = RandomTeamGenerator()
    team0 = team_gen.get_team()
    team1 = team_gen.get_team()
    print(a.get_action((get_full_team_view(team0), get_full_team_view(team1))))


if __name__ == '__main__':
    main()
