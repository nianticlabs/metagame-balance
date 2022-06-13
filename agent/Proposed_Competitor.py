from vgc.behaviour import BattlePolicy, TeamSelectionPolicy
from vgc.behaviour.BattlePolicies import GUIBattlePolicy, RandomBattlePolicy
from vgc.behaviour.BalancePolicies import BalancePolicy 
from vgc.behaviour.TeamSelectionPolicies import GUITeamSelectionPolicy
from vgc.competition.Competitor import Competitor
from policies.CMAESBalancePolicy import CMAESBalancePolicy

class ProposedCompetitor(Competitor):

    def __init__(self, name: str = "Niantic Policy"):
        self._name = name
        self._balance_policy = CMAESBalancePolicy()

    @property
    def name(self):
        return self._name

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy

    @property
    def balance_policy(self) -> BalancePolicy:
        return self._balance_policy
