from typing import Tuple

from framework.DataObjects import PkmTeamPrediction, PkmTeamView, MetaData
from framework.behaviour import TeamPredictor


class NullTeamPredictor(TeamPredictor):

    null_team_prediction = PkmTeamPrediction()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmTeamView, MetaData]) -> PkmTeamPrediction:
        return NullTeamPredictor.null_team_prediction
