from typing import List

from metagame_balance.policies.FixedTeamPolicy import FixedTeamPolicy
from metagame_balance.vgc.behaviour import TeamBuildPolicy, BattlePolicy
from metagame_balance.vgc.behaviour.BattlePolicies import BetterRandomBattlePolicy
from metagame_balance.vgc.competition.Competitor import Competitor


class FixedTeamCompetitor(Competitor):
    def __init__(self, name:str, team: List, utility_manager = None):
        self._name = name
        self._battle_policy = BetterRandomBattlePolicy()
        self._team_build_policy = FixedTeamPolicy() #create a policy based on U!
        self._team_build_policy.set_team(team)

    @property
    def name(self):
        return self._name

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return self._team_build_policy

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy


