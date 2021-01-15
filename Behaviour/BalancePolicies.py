from Behaviour import BalancePolicy
from Framework.DataObjects import PkmRoster


class IdleBalancePolicy(BalancePolicy):

    def requires_encode(self) -> bool:
        pass

    def close(self):
        pass

    def get_action(self, s) -> PkmRoster:
        return s
