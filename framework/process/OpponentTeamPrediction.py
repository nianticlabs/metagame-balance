from framework.behaviour.TeamPredictors import TeamPredictor, NullTeamPredictor
from framework.DataObjects import MetaData, PkmTeamPrediction, PkmFullTeamView


class OpponentTeamPrediction:

    def __init__(self, tp: TeamPredictor, meta_data: MetaData, opp_view: PkmFullTeamView):
        self.__tp = tp
        self.__meta_data = meta_data
        self.__opp_view = opp_view
        # output
        self.__team_prediction = NullTeamPredictor.null_team_prediction

    def run(self):
        try:
            self.__team_prediction = self.__tp.get_action((self.__opp_view, self.__meta_data))
        except:
            self.__team_prediction = NullTeamPredictor.null_team_prediction

    @property
    def team_prediction(self) -> PkmTeamPrediction:
        return self.__team_prediction
