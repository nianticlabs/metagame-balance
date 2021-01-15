from typing import Any
from Behaviour import DataAggregator


class NullDataAggregator(DataAggregator):

        def requires_encode(self) -> bool:
            pass

        def close(self):
            pass

        def get_action(self, s) -> Any:
            return None
