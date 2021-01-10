from copy import deepcopy
from random import sample
from Behaviour import SelectorPolicy
from Framework.Competition.Config import TEAM_SIZE
from Framework.DataObjects import PkmTeam, MetaData


class TeamSelection:

    def __init__(self, sp: SelectorPolicy, team: PkmTeam, meta_data: MetaData, opp):  # TODO opp
        self.sp = sp
        self.team = team
        self.meta_data = meta_data
        self.opp = opp

    def get_selected_team(self) -> PkmTeam:
        team = deepcopy(self.team)
        data = deepcopy(self.team)
        team_ids = list(self.sp.get_action((team, self.opp, data)))
        # if returned team is bigger than allowed
        if len(team_ids) > TEAM_SIZE:
            team_ids = team_ids[:TEAM_SIZE]
        # if returned team is smaller than allowed or repeated elements
        if len(team_ids) < TEAM_SIZE:
            team_ids = sample(range(6), TEAM_SIZE)
        selected_team = self.team.select_team(team_ids)
        return selected_team
