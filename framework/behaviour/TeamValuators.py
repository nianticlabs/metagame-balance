from typing import Tuple
from framework.DataObjects import TeamValue, PkmFullTeam, MetaData
from framework.behaviour import TeamValuator


class NullTeamValuator(TeamValuator):

    class NullTeamValue(TeamValue):

        def compare_to(self, value) -> int:
            return 0

    null_team_value = NullTeamValue()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmFullTeam, MetaData]) -> TeamValue:
        return NullTeamValuator.null_team_value
