from random import sample
from framework.behaviour import SelectorPolicy
from framework.DataConstants import DEFAULT_TEAM_SIZE
from framework.DataObjects import PkmTeam, MetaData, PkmTeamHypothesis, PkmFullTeam, get_full_team_view


class TeamSelection:

    def __init__(self, sp: SelectorPolicy, full_team: PkmFullTeam, opp_team: PkmFullTeam, meta_data: MetaData,
                 opp_hypothesis: PkmTeamHypothesis):
        self.sp = sp
        self.full_team = full_team
        self.full_team_view = get_full_team_view(full_team)
        self.opp_team = get_full_team_view(opp_team, team_hypothesis=opp_hypothesis, partial=True)
        self.meta_data = meta_data

    def get_selected_team(self) -> PkmTeam:
        try:
            team_ids = list(self.sp.get_action((self.full_team_view, self.opp_team, self.meta_data)))
        except:
            team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
        # if returned team is bigger than allowed
        if len(team_ids) > DEFAULT_TEAM_SIZE:
            team_ids = team_ids[:DEFAULT_TEAM_SIZE]
        # if returned team is smaller than allowed or repeated elements
        if len(team_ids) < DEFAULT_TEAM_SIZE:
            team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
        return self.full_team.get_battle_team(team_ids)
