from typing import Tuple
from framework.DataObjects import TeamValuation, PkmFullTeam, MetaData
from framework.behaviour import TeamValuator


class NullTeamValuator(TeamValuator):

    null_team_valuation = TeamValuation()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmFullTeam, MetaData]) -> TeamValuation:
        return NullTeamValuator.null_team_valuation
