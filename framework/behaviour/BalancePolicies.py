from typing import Tuple
from framework.behaviour import BalancePolicy
from framework.DataObjects import PkmRoster, MetaData, DesignConstraints


class IdleBalancePolicy(BalancePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> PkmRoster:
        return d[0]
