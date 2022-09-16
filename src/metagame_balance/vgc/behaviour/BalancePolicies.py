from typing import Tuple

from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.balance.restriction import DesignConstraints
from metagame_balance.vgc.behaviour import BalancePolicy
from metagame_balance.vgc.datatypes.Objects import PkmRoster


class IdleBalancePolicy(BalancePolicy):

    def __init__(self):
        self.dr = DeltaRoster({})

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> DeltaRoster:
        return self.dr
