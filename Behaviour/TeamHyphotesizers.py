from Behaviour import TeamHyphotesizer
from Framework.DataObjects import PkmTeam


class NullTeamHyphotesizer(TeamHyphotesizer):

    null_team = PkmTeam()

    def get_action(self, s) -> PkmTeam:
        return NullTeamHyphotesizer.null_team
