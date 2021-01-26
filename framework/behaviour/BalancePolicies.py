from framework.behaviour import BalancePolicy
from framework.DataObjects import PkmRoster


class IdleBalancePolicy(BalancePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> PkmRoster:
        return s
