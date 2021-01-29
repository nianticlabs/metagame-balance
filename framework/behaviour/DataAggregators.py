from typing import Any

from framework.DataObjects import MetaData
from framework.behaviour import DataAggregator


class NullDataAggregator(DataAggregator):

    null_meta_data = MetaData()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> MetaData:
        return NullDataAggregator.null_meta_data
