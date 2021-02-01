from framework.behaviour import DataAggregator
from framework.DataObjects import MetaData
from framework.util.Recording import GamePlayRecorder


class DataAggregation:

    def __init__(self, da: DataAggregator, meta_data: MetaData, rec: GamePlayRecorder):
        self.__da = da
        self.__meta_data = meta_data
        self.__rec = rec

    def run(self):
        try:
            self.__da.get_action((self.__meta_data, self.__rec))
        except:
            pass
