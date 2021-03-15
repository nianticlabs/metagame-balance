from framework.DataObjects import MetaData, PkmFullTeam, PkmRoster, get_pkm_roster_view, TeamValue
from framework.behaviour import TeamBuilderPolicy
from framework.competition import legal_team
from framework.util.PkmTeamGenerators import RandomGeneratorRoster


class TeamBuilding:

    def __init__(self, tbp: TeamBuilderPolicy, full_team: PkmFullTeam, meta_data: MetaData, roster: PkmRoster):
        self.__tbp = tbp
        self.__full_team = full_team
        self.__meta_data = meta_data
        self.__roster = roster
        self.__roster_view = get_pkm_roster_view(self.__roster)
        # output
        self.__team = None
        self.__rand_gen = RandomGeneratorRoster(self.__roster)

    def run(self, val: TeamValue):
        try:
            self.__team = self.__tbp.get_action((self.__meta_data, self.__full_team, self.__roster_view, val))
            if not legal_team(self.__team, self.__roster):
                self.__team = self.__rand_gen.get_team()
        except:
            self.__team = self.__full_team

    @property
    def team(self) -> PkmFullTeam:
        return self.__team
