from framework.balance.meta import MetaData
from framework.behaviour import TeamBuilderPolicy
from framework.competition import legal_team
from framework.datatypes.Objects import PkmFullTeam, PkmRoster, get_pkm_roster_view, TeamValue
from framework.util.generator.PkmTeamGenerators import RandomGeneratorRoster


class TeamBuilding:

    def __init__(self, tbp: TeamBuilderPolicy, full_team: PkmFullTeam, meta_data: MetaData, roster: PkmRoster):
        self.tbp = tbp
        self.full_team = full_team
        self.meta_data = meta_data
        self.roster = roster
        self.roster_view = get_pkm_roster_view(self.roster)
        # output
        self.team = None
        self.rand_gen = RandomGeneratorRoster(self.roster)

    def run(self, val: TeamValue):
        try:
            self.team = self.tbp.get_action((self.meta_data, self.full_team, self.roster_view, val))
            if not legal_team(self.team, self.roster):
                self.team = self.rand_gen.get_team()
        except:
            self.team = self.full_team
