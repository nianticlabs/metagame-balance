from typing import Dict

from framework.datatypes.Objects import PkmRoster, PkmMove, PkmTemplate


class DeltaPkm:

    def __init__(self, pkm: PkmTemplate, dpm: Dict[int, PkmMove]):
        self.max_hp = pkm.max_hp
        self.type = pkm.type
        self.dpm = dpm

    def apply(self, pkm: PkmTemplate):
        pkm.max_hp = self.max_hp
        pkm.type = self.type
        for idx, move in enumerate(pkm.move_roster):
            if idx in self.dpm.keys():
                dpm = self.dpm[idx]
                move.__dict__.update(dpm.__dict__)


class DeltaRoster:

    def __init__(self, dp: Dict[int, DeltaPkm]):
        self.dp = dp

    def apply(self, roster: PkmRoster):
        for idx, pkm in enumerate(roster):
            if idx in self.dp.keys():
                self.dp[idx].apply(pkm)
