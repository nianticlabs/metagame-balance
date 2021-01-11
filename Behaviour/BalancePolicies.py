from Behaviour import BalancePolicy
from Framework.DataObjects import PkmRoster


class IdleBalancePolicy(BalancePolicy):

    def get_action(self, s) -> PkmRoster:
        return s
