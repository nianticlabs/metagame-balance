from random import sample
from framework.DataObjects import PkmTeam, MetaData, PkmFullTeam
from framework.behaviour import BattlePolicy
from framework.behaviour.DataAggregators import NullDataAggregator
from framework.competition.CompetitionObjects import Competitor


class ExampleBattlePolicy(BattlePolicy):

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, s) -> int:
        return sample(range(4 + 3), 1)[0]


class Example(Competitor):

    def __init__(self, name: str = "Example", team: PkmFullTeam = None):
        self._name = name
        self._battle_policy = ExampleBattlePolicy()
        self._team = team

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
        return NullDataAggregator.null_metadata

    def want_to_change_team(self):
        pass

    @property
    def team(self) -> PkmFullTeam:
        return self._team

    @team.setter
    def team(self, team: PkmFullTeam):
        self._team = team
