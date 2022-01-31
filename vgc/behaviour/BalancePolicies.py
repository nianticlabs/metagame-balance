from typing import Tuple

from vgc.balance import DeltaRoster
from vgc.balance.meta import MetaData
from vgc.balance.restriction import DesignConstraints
from vgc.behaviour import BalancePolicy
from vgc.datatypes.Objects import PkmRoster


class IdleBalancePolicy(BalancePolicy):

    def __init__(self):
        self.dr = DeltaRoster({})

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> DeltaRoster:
        return self.dr
