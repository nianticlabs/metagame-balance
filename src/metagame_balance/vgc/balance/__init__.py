from typing import Dict

from metagame_balance.vgc.datatypes.Objects import PkmRoster, PkmMove, PkmTemplate
from metagame_balance.vgc.datatypes.Types import PkmType


class DeltaPkm:

    def __init__(self, max_hp: float, pkm_type: PkmType, dpm: Dict[int, PkmMove]):
        self.max_hp = max_hp
        self.type = pkm_type
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
        for pkm in roster:
            if pkm.pkm_id in self.dp.keys():
                self.dp[pkm.pkm_id].apply(pkm)
