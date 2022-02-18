from abc import ABC

from vgc.behaviour import BattlePolicy, TeamSelectionPolicy, TeamBuildPolicy, TeamPredictor, BalancePolicy
from vgc.behaviour.BalancePolicies import IdleBalancePolicy
from vgc.behaviour.BattlePolicies import RandomBattlePolicy
from vgc.behaviour.TeamBuildPolicies import RandomTeamBuildPolicy
from vgc.behaviour.TeamPredictors import NullTeamPredictor
from vgc.behaviour.TeamSelectionPolicies import RandomTeamSelectionPolicy

random_battle_policy = RandomBattlePolicy()
random_selector_policy = RandomTeamSelectionPolicy()
random_team_build_policy = RandomTeamBuildPolicy()
idle_balance_policy = IdleBalancePolicy()
null_team_predictor = NullTeamPredictor()


class Competitor(ABC):

    @property
    def battle_policy(self) -> BattlePolicy:
        return random_battle_policy

    @property
    def team_selection_policy(self) -> TeamSelectionPolicy:
        return random_selector_policy

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return random_team_build_policy

    @property
    def team_predictor(self) -> TeamPredictor:
        return null_team_predictor

    @property
    def balance_policy(self) -> BalancePolicy:
        return idle_balance_policy

    @property
    def name(self) -> str:
        return ""
