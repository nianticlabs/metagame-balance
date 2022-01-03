from framework.balance.meta import MetaData
from framework.behaviour import DataAggregator
from framework.util.Recording import MetaGameSubscriber


class DataAggregation:

    def __init__(self, da: DataAggregator, meta_data: MetaData, mgs: MetaGameSubscriber):
        self.__da = da
        self.__meta_data = meta_data
        self.__mgs = mgs

    # noinspection PyBroadException
    def run(self):
        try:
            self.__da.get_action((self.__meta_data, self.__mgs))
        except:
            pass
