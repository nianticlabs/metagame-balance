from framework.behaviour import TeamHyphotesizer
from framework.DataObjects import PkmTeamHypothesis


class NullTeamHyphotesizer(TeamHyphotesizer):

    null_team_hypothesis = PkmTeamHypothesis()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> PkmTeamHypothesis:
        return NullTeamHyphotesizer.null_team_hypothesis
