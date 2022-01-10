from abc import ABC

from framework.behaviour import BattlePolicy, TeamSelectionPolicy, TeamBuildPolicy, TeamPredictor, TeamValuator, \
    BalancePolicy
from framework.behaviour.BalancePolicies import IdleBalancePolicy
from framework.behaviour.BattlePolicies import RandomBattlePolicy
from framework.behaviour.TeamBuildPolicies import RandomTeamBuildPolicy
from framework.behaviour.TeamPredictors import NullTeamPredictor
from framework.behaviour.TeamSelectionPolicies import RandomTeamSelectionPolicy
from framework.behaviour.TeamValuators import NullTeamValuator

random_battle_policy = RandomBattlePolicy()
random_selector_policy = RandomTeamSelectionPolicy()
random_builder_policy = RandomTeamBuildPolicy()
idle_balance_policy = IdleBalancePolicy()
null_team_predictor = NullTeamPredictor()
null_team_valuator = NullTeamValuator()


class Competitor(ABC):

    @property
    def battle_policy(self) -> BattlePolicy:
        return random_battle_policy

    @property
    def team_selection_policy(self) -> TeamSelectionPolicy:
        return random_selector_policy

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return random_builder_policy

    @property
    def team_predictor(self) -> TeamPredictor:
        return null_team_predictor

    @property
    def team_valuator(self) -> TeamValuator:
        return null_team_valuator

    @property
    def balance_policy(self) -> BalancePolicy:
        return idle_balance_policy

    @property
    def name(self) -> str:
        return ""
