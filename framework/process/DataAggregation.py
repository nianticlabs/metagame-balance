from framework.balance.meta import MetaData
from framework.behaviour import DataAggregator
from framework.util.Recording import MetaGameSubscriber


class DataAggregation:

    def __init__(self, da: DataAggregator, meta_data: MetaData, mgs: MetaGameSubscriber):
        self.da = da
        self.meta_data = meta_data
        self.mgs = mgs

    # noinspection PyBroadException
    def run(self):
        try:
            self.da.get_action((self.meta_data, self.mgs))
        except:
            pass
