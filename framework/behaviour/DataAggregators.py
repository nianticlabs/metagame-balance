from framework.DataObjects import MetaData
from framework.behaviour import DataAggregator


class NullDataAggregator(DataAggregator):

    class NullMetaData(MetaData):
        pass

    null_metadata = NullMetaData()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> MetaData:
        return NullDataAggregator.null_metadata
