from framework.behaviour import TeamHyphotesizer
from framework.DataObjects import PkmTeam


class NullTeamHyphotesizer(TeamHyphotesizer):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    null_team = PkmTeam()

    def get_action(self, s) -> PkmTeam:
        return NullTeamHyphotesizer.null_team
