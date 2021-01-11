from copy import deepcopy
from typing import Any

from Behaviour import TeamValuator
from Framework.DataObjects import MetaData


class TeamValuation:

    def __init__(self, tv: TeamValuator, meta_data: MetaData):
        self.tv = tv
        self.meta_data = meta_data

    def get_team_valuation(self) -> Any:
        meta_data = deepcopy(self.meta_data)
        try:
            val = self.tv.get_action(meta_data)
        except:
            return None
        return val
