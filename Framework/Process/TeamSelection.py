from copy import deepcopy
from random import sample
from Behaviour import SelectorPolicy
from Framework.DataConstants import DEFAULT_TEAM_SIZE
from Framework.DataObjects import PkmTeam, MetaData


class TeamSelection:

    def __init__(self, sp: SelectorPolicy, team: PkmTeam, meta_data: MetaData, opp):  # TODO opp
        self.sp = sp
        self.team = team
        self.meta_data = meta_data
        self.opp = opp

    def get_selected_team(self) -> PkmTeam:
        team = deepcopy(self.team)
        meta_data = deepcopy(self.meta_data)
        try:
            team_ids = list(self.sp.get_action((team, self.opp, meta_data)))
        except:
            team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
        # if returned team is bigger than allowed
        if len(team_ids) > DEFAULT_TEAM_SIZE:
            team_ids = team_ids[:DEFAULT_TEAM_SIZE]
        # if returned team is smaller than allowed or repeated elements
        if len(team_ids) < DEFAULT_TEAM_SIZE:
            team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
        selected_team = self.team.select_team(team_ids)
        return selected_team
