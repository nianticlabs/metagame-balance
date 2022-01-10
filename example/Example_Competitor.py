from framework.behaviour import BattlePolicy, TeamSelectionPolicy
from framework.behaviour.BattlePolicies import GUIBattlePolicy, RandomBattlePolicy
from framework.behaviour.TeamSelectionPolicies import GUITeamSelectionPolicy
from framework.competition.Competitor import Competitor


class ExampleCompetitor(Competitor):

    def __init__(self, name: str = "Example"):
        self._name = name
        self._battle_policy = RandomBattlePolicy()

    @property
    def name(self):
        return self._name

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy


class GUIExampleCompetitor(ExampleCompetitor):

    def __init__(self, name: str = ""):
        super().__init__(name)

    @property
    def team_selection_policy(self) -> TeamSelectionPolicy:
        return GUITeamSelectionPolicy()

    @property
    def battle_policy(self) -> BattlePolicy:
        return GUIBattlePolicy()
