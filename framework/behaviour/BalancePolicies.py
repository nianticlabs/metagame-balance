from typing import Tuple

from framework.balance import DeltaRoster
from framework.balance.meta import MetaData
from framework.balance.restriction import DesignConstraints
from framework.behaviour import BalancePolicy
from framework.datatypes.Objects import PkmRoster


class IdleBalancePolicy(BalancePolicy):

    def __init__(self):
        self.dr = DeltaRoster({})

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> DeltaRoster:
        return self.dr
