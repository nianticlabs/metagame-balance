from typing import Any
from framework.behaviour import TeamValuator


class NullTeamValuator(TeamValuator):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> Any:
        return None
