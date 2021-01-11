from copy import deepcopy

from Behaviour import TeamHyphotesizer
from Behaviour.TeamHyphotesizers import NullTeamHyphotesizer
from Framework.DataObjects import MetaData


class OponentTeamHyphotesizing:

    def __init__(self, th: TeamHyphotesizer, meta_data: MetaData, opp, traj):  # TODO opp
        self.th = th
        self.meta_data = meta_data
        self.opp = opp
        self.traj = traj

    def get_team_hyphothesis(self):  # TODO opp
        meta_data = deepcopy(self.meta_data)
        traj = deepcopy(self.traj)
        try:
            h = self.th.get_action((self.opp, meta_data, traj))
        except:
            return NullTeamHyphotesizer.null_team
        return h
