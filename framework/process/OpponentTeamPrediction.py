from framework.balance.meta import MetaData
from framework.behaviour.TeamPredictors import TeamPredictor, NullTeamPredictor
from framework.datatypes.Objects import PkmFullTeamView


class OpponentTeamPrediction:

    def __init__(self, tp: TeamPredictor, meta_data: MetaData, opp_view: PkmFullTeamView):
        self.tp = tp
        self.meta_data = meta_data
        self.opp_view = opp_view
        # output
        self.team_prediction = NullTeamPredictor.null_team_prediction

    # noinspection PyBroadException
    def run(self):
        try:
            self.team_prediction = self.tp.get_action((self.opp_view, self.meta_data))
        except:
            self.team_prediction = NullTeamPredictor.null_team_prediction
