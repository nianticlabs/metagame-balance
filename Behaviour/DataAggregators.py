from typing import Any
from Behaviour import DataAggregator


class NullDataAggregator(DataAggregator):

        def get_action(self, s) -> Any:
            return None
