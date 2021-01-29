from framework.behaviour import DataAggregator
from framework.DataObjects import MetaData
from framework.util.Recording import GamePlayRecorder


class DataAggregation:

    def __init__(self, da: DataAggregator, meta_data: MetaData, rec: GamePlayRecorder):
        self.da = da
        self.meta_data = meta_data
        self.rec = rec

    def run(self):
        try:
            self.da.get_action((self.meta_data, self.rec))
        except:
            pass
