from Behaviour import BattlePolicy
from Framework.Competition.CompetitionObjects import Competitor


class BattlePolicy2(BattlePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> int:
        return 2000


class Competitor2(Competitor):

    def get_battle_policy(self) -> BattlePolicy:
        return BattlePolicy2()
