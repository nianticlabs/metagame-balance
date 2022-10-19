from typing import Tuple, Optional, List
import random

from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.behaviour import TeamSelectionPolicy, BattlePolicy, TeamBuildPolicy
from metagame_balance.vgc.behaviour.BattlePolicies import BetterRandomBattlePolicy
from metagame_balance.vgc.behaviour.TeamSelectionPolicies import RandomTeamSelectionPolicy
from metagame_balance.vgc.competition.Competitor import Competitor
from metagame_balance.vgc.datatypes.Objects import PkmFullTeam, PkmRosterView, PkmRoster, Pkm


class FixedSizeRandomTeamBuildPolicy(TeamBuildPolicy):
    """
    Picks a random team from the full roster.
    """
    def __init__(self, team_size: int):
        super(FixedSizeRandomTeamBuildPolicy, self).__init__()
        self.team_size = team_size

    def get_action(self, s: Tuple[MetaData, Optional[PkmFullTeam], PkmRoster]) -> PkmFullTeam:
        roster = s[2]
        selected = random.sample(list(roster), self.team_size)
        team: List[Pkm] = [s.gen_pkm() for s in selected]
        return PkmFullTeam(team)

    def close(self):
        pass


class RandomTeamSelectionCompetitor(Competitor):
    def __init__(self, team_size: int):
        self.team_size = team_size
        self._team_build_policy = FixedSizeRandomTeamBuildPolicy(team_size)
        self._team_selection_policy = RandomTeamSelectionPolicy(teams_size=team_size, selection_size=team_size)
        self._battle_policy = BetterRandomBattlePolicy()

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return self._team_build_policy

    @property
    def team_selection_policy(self) -> TeamSelectionPolicy:
        return self._team_selection_policy

    @property
    def name(self):
        return "RandomTeamSelectionCompetitor"

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy
