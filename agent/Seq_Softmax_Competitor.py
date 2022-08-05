from vgc.behaviour import TeamBuildPolicy, BattlePolicy
from vgc.competition.Competitor import Competitor
from Utility_Fn_Manager import UtilityFunctionManager
from policies.SeqSoftmaxSelectionPolicy import SeqSoftmaxSelectionPolicy
from vgc.behaviour.BattlePolicies import BetterRandomBattlePolicy

class SeqSoftmaxCompetitor(Competitor):

    def __init__(self, name: str, utility_manager: UtilityFunctionManager):
        self._name = name
        if name == 'adversary':
            self.get_u_fn = utility_manager.adversary_U_function
            update_policy = False
        else:
            self.get_u_fn = utility_manager.agent_U_function
            update_policy = True
        self._team_build_policy = SeqSoftmaxSelectionPolicy(utility_manager, self.get_u_fn, update_policy) #create a policy based on U!
        self._battle_policy = BetterRandomBattlePolicy()

    @property
    def name(self):
        return self._name

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return self._team_build_policy

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy

