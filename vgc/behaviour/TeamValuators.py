from typing import Tuple

from vgc.balance.meta import MetaData
from vgc.behaviour import TeamValuator
from vgc.datatypes.Objects import TeamValue, PkmFullTeam


class NullTeamValuator(TeamValuator):
    class NullTeamValue(TeamValue):

        def compare_to(self, value) -> int:
            return 0

    null_team_value = NullTeamValue()

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmFullTeam, MetaData]) -> TeamValue:
        return NullTeamValuator.null_team_value
