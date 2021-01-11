from copy import deepcopy
from typing import Any

from Behaviour import DataAggregator
from Framework.DataObjects import MetaData


class DataAggregation:

    def __init__(self, da: DataAggregator, meta_data: MetaData, traj):
        self.da = da
        self.meta_data = meta_data
        self.traj = traj

    def get_team_hyphothesis(self) -> Any:
        meta_data = deepcopy(self.meta_data)
        traj = deepcopy(self.traj)
        try:
            h = self.da.get_action((meta_data, traj))
        except:
            return None
        return h
