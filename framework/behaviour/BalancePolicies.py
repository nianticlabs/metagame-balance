from typing import Tuple

from framework.balance.meta import MetaData
from framework.balance.restriction import DesignConstraints
from framework.behaviour import BalancePolicy
from framework.datatypes.Objects import PkmRoster


class IdleBalancePolicy(BalancePolicy):

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> PkmRoster:
        return d[0]
