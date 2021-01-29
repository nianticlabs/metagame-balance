from framework.behaviour import TeamBuilderPolicy
from framework.DataObjects import MetaData, PkmFullTeam, PkmRoster, get_pkm_roster_view, TeamValue


class TeamBuilding:

    def __init__(self, tbp: TeamBuilderPolicy, full_team: PkmFullTeam, meta_data: MetaData, roster: PkmRoster,
                 val: TeamValue):
        self.__tbp = tbp
        self.__full_team = full_team
        self.__meta_data = meta_data
        self.__roster_view = get_pkm_roster_view(roster)
        self.__val = val
        # output
        self.__team = None

    def run(self):
        try:
            self.__team = self.__tbp.get_action((self.__meta_data, self.__full_team, self.__roster_view, self.__val))
        except:
            self.__team = self.__full_team

    @property
    def team(self) -> PkmFullTeam:
        return self.__team
