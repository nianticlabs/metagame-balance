from typing import Any
from Behaviour import TeamValuator


class NullTeamValuator(TeamValuator):

    def get_action(self, s) -> Any:
        return None
