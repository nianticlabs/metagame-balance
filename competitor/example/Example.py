from framework.DataObjects import PkmTeam, MetaData
from framework.behaviour import BattlePolicy
from framework.competition.CompetitionObjects import Competitor, null_metadata


class ExampleBattlePolicy(BattlePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> int:
        return 1000


class Example(Competitor):

    def __init__(self):
        self._name = "Example"
        self._battle_policy = ExampleBattlePolicy()
        self._team = None

    @property
    def name(self):
        return self._name

    def reset(self):
        pass

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy

    @property
    def meta_data(self) -> MetaData:
        return null_metadata

    def want_to_change_team(self):
        pass

    @property
    def team(self) -> PkmTeam:
        return self._team

    @team.setter
    def team(self, team):
        self._team = team
