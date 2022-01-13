from typing import Tuple

from framework.balance.meta import MetaData
from framework.behaviour import TeamValuator
from framework.datatypes.Objects import TeamValue, PkmFullTeam


class NullTeamValuator(TeamValuator):
    class NullTeamValue(TeamValue):

        def compare_to(self, value) -> int:
            return 0

    null_team_value = NullTeamValue()

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmFullTeam, MetaData]) -> TeamValue:
        return NullTeamValuator.null_team_value
