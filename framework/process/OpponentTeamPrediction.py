from framework.behaviour.TeamPredictors import TeamPredictor, NullTeamPredictor
from framework.DataObjects import MetaData, PkmTeamPrediction, PkmFullTeamView


class OpponentTeamPrediction:

    def __init__(self, tp: TeamPredictor, meta_data: MetaData, opp_view: PkmFullTeamView):
        self.tp = tp
        self.meta_data = meta_data
        self.opp_view = opp_view

    def get_team_hyphothesis(self) -> PkmTeamPrediction:
        try:
            h = self.tp.get_action((self.opp_view, self.meta_data))
        except:
            return NullTeamPredictor.null_team_hypothesis
        return h
