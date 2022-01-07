from abc import ABC, abstractmethod

from numpy.random import sample

from framework.behaviour import BattlePolicy, SelectorPolicy, TeamBuilderPolicy, TeamPredictor, TeamValuator, \
    BalancePolicy
from framework.behaviour.BalancePolicies import IdleBalancePolicy
from framework.behaviour.BattlePolicies import RandomBattlePolicy, GUIBattlePolicy
from framework.behaviour.SelectorPolicies import RandomSelectorPolicy, GUISelectorPolicy
from framework.behaviour.TeamBuilderPolicies import RandomTeamBuilderPolicy
from framework.behaviour.TeamPredictors import NullTeamPredictor
from framework.behaviour.TeamValuators import NullTeamValuator
from framework.datatypes.Objects import PkmFullTeam

random_battle_policy = RandomBattlePolicy()
random_selector_policy = RandomSelectorPolicy()
random_builder_policy = RandomTeamBuilderPolicy()
idle_balance_policy = IdleBalancePolicy()
null_team_predictor = NullTeamPredictor()
null_team_valuator = NullTeamValuator()


class Competitor(ABC):

    @property
    def battle_policy(self) -> BattlePolicy:
        return random_battle_policy

    @property
    def selector_policy(self) -> SelectorPolicy:
        return random_selector_policy

    @property
    def team_builder_policy(self) -> TeamBuilderPolicy:
        return random_builder_policy

    @property
    def team_prediction_policy(self) -> TeamPredictor:
        return null_team_predictor

    @property
    def team_valuator_policy(self) -> TeamValuator:
        return null_team_valuator

    @property
    def balance_policy(self) -> BalancePolicy:
        return idle_balance_policy

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class ExampleBattlePolicy(BattlePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> int:
        return sample(range(4 + 3), 1)[0]


class ExampleCompetitor(Competitor):

    def __init__(self, name: str = "Example", team: PkmFullTeam = None):
        self._name = name
        self._battle_policy = ExampleBattlePolicy()
        self._team = team

    @property
    def name(self):
        return self._name

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy


class GUIExampleCompetitor(ExampleCompetitor):

    def __init__(self, team: PkmFullTeam, name: str = ""):
        super().__init__(name, team)

    @property
    def selector_policy(self) -> SelectorPolicy:
        return GUISelectorPolicy()

    @property
    def battle_policy(self) -> BattlePolicy:
        return GUIBattlePolicy()
