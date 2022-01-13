from typing import Tuple

from framework.balance.meta import MetaData
from framework.behaviour import TeamPredictor
from framework.datatypes.Objects import PkmTeamPrediction, PkmTeamView


class NullTeamPredictor(TeamPredictor):
    null_team_prediction = PkmTeamPrediction()

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmTeamView, MetaData]) -> PkmTeamPrediction:
        return NullTeamPredictor.null_team_prediction
