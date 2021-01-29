from random import sample
from framework.behaviour import SelectorPolicy
from framework.DataConstants import DEFAULT_TEAM_SIZE
from framework.DataObjects import PkmTeam, PkmTeamPrediction, PkmFullTeam, get_full_team_view


class TeamSelection:

    def __init__(self, sp: SelectorPolicy, full_team: PkmFullTeam, opp_full_team: PkmFullTeam,
                 opp_prediction: PkmTeamPrediction):
        self.__sp = sp
        self.__full_team = full_team
        self.__full_team_view = get_full_team_view(full_team)
        self.__full_opp_team_view = get_full_team_view(opp_full_team, team_prediction=opp_prediction, partial=True)
        # output
        self.__team_ids = []

    def run(self):
        try:
            self.__team_ids = list(self.__sp.get_action((self.__full_team_view, self.__full_opp_team_view)))
        except:
            self.__team_ids = sample(range(6), DEFAULT_TEAM_SIZE)
        # if returned team is bigger than allowed
        if len(self.__team_ids) > DEFAULT_TEAM_SIZE:
            self.__team_ids = self.__team_ids[:DEFAULT_TEAM_SIZE]
        # if returned team is smaller than allowed or repeated elements
        if len(self.__team_ids) < DEFAULT_TEAM_SIZE:
            self.__team_ids = sample(range(6), DEFAULT_TEAM_SIZE)

    @property
    def selected_team(self) -> PkmTeam:
        return self.__full_team.get_battle_team(self.__team_ids)
