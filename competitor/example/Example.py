from framework.behaviour import BattlePolicy
from framework.competition.CompetitionObjects import Competitor


class ExampleBattlePolicy(BattlePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> int:
        return 1000


class Example(Competitor):

    def __init__(self):
        self._name = "Example"
        self._battle_policy = ExampleBattlePolicy()

    @property
    def name(self):
        return self._name

    def reset(self):
        pass

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy
