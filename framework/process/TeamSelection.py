from random import sample
from framework.behaviour import SelectorPolicy
from framework.DataConstants import DEFAULT_TEAM_SIZE
from framework.DataObjects import PkmTeam, PkmTeamPrediction, PkmFullTeam, get_full_team_view


class TeamSelection:

    def __init__(self, sp: SelectorPolicy, full_team: PkmFullTeam, opp_full_team: PkmFullTeam,
                 opp_hypothesis: PkmTeamPrediction):
        self.sp = sp
        self.full_team = full_team
        self.full_team_view = get_full_team_view(full_team)
        self.full_opp_team_view = get_full_team_view(opp_full_team, team_prediction=opp_hypothesis, partial=True)

    def get_selected_team(self) -> PkmTeam:
        try:
            team_ids = list(self.sp.get_action((self.full_team_view, self.full_opp_team_view)))
        except:
            team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
        # if returned team is bigger than allowed
        if len(team_ids) > DEFAULT_TEAM_SIZE:
            team_ids = team_ids[:DEFAULT_TEAM_SIZE]
        # if returned team is smaller than allowed or repeated elements
        if len(team_ids) < DEFAULT_TEAM_SIZE:
            team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
        return self.full_team.get_battle_team(team_ids)
