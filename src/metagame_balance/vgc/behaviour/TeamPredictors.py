from typing import Tuple

from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.behaviour import TeamPredictor
from metagame_balance.vgc.datatypes.Objects import PkmTeamPrediction, PkmTeamView


class NullTeamPredictor(TeamPredictor):
    null_team_prediction = PkmTeamPrediction()

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmTeamView, MetaData]) -> PkmTeamPrediction:
        return NullTeamPredictor.null_team_prediction
