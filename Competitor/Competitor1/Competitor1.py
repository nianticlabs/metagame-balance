from Behaviour import BattlePolicy
from Framework.Competition.CompetitionObjects import Competitor


class BattlePolicy1(BattlePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> int:
        return 1000


class Competitor1(Competitor):

    def get_battle_policy(self) -> BattlePolicy:
        return BattlePolicy1()
