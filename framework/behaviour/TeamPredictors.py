from typing import Tuple
from framework.behaviour import TeamPredictor
from framework.DataObjects import PkmTeamPrediction, PkmTeamView, MetaData


class NullTeamPredictor(TeamPredictor):

    null_team_hypothesis = PkmTeamPrediction()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmTeamView, MetaData]) -> PkmTeamPrediction:
        return NullTeamPredictor.null_team_hypothesis
