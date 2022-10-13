from metagame_balance.vgc.behaviour import TeamBuildPolicy, BattlePolicy, TeamSelectionPolicy
from metagame_balance.vgc.behaviour.TeamSelectionPolicies import RandomTeamSelectionPolicy
from metagame_balance.vgc.competition.Competitor import Competitor
from metagame_balance.utility import UtilityFunctionManager
from metagame_balance.policies.SeqSoftmaxSelectionPolicy import SeqSoftmaxSelectionPolicy
from metagame_balance.vgc.behaviour.BattlePolicies import BetterRandomBattlePolicy


class SeqSoftmaxCompetitor(Competitor):
    """
    Competitor that uses sequential softmax to determine how to form the team from the whole roster, and uses a random
    policy to determine what order to send pokemon out.
    """
    def __init__(self, name: str, utility_manager: UtilityFunctionManager, team_size: int):
        self._name = name
        update_policy = True
        if name == 'adversary':
            self.get_u_fn = utility_manager.adversary_U_function
        else:
            self.get_u_fn = utility_manager.agent_U_function
        self._team_build_policy = SeqSoftmaxSelectionPolicy(utility_manager, self.get_u_fn, update_policy, team_size) #create a policy based on U!
        self._battle_policy = BetterRandomBattlePolicy()
        # note. we assume that the whole team will be selected to battle, and that this isn't a pokemon stadium type
        # of thing where you pick 3 out of 6 and send them out.
        self._team_selection_policy = RandomTeamSelectionPolicy(teams_size=team_size, selection_size=team_size)

    @property
    def name(self):
        return self._name

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return self._team_build_policy

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy

    @property
    def team_selection_policy(self) -> TeamSelectionPolicy:
        return self._team_selection_policy

