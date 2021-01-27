from framework.behaviour import TeamHyphotesizer
from framework.DataObjects import PkmTeamHypothesis


class NullTeamHyphotesizer(TeamHyphotesizer):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    null_team_hypothesis = PkmTeamHypothesis()

    def get_action(self, s) -> PkmTeamHypothesis:
        return NullTeamHyphotesizer.null_team_hypothesis
