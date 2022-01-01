""" Remote Clients """
from multiprocessing.connection import Client
from typing import Set

from framework.DataObjects import PkmFullTeam, PkmTeamPrediction, MetaData, TeamValue, PkmRoster
from framework.behaviour import BattlePolicy, SelectorPolicy, TeamBuilderPolicy, TeamPredictor, DataAggregator, \
    TeamValuator, BalancePolicy
from framework.competition.CompetitionObjects import Competitor


ENCODE_TIMEOUT = 1.0
CLOSE_TIMEOUT = 1.0


class ProxyBattlePolicy(BattlePolicy):

    def __init__(self, conn: Client, timeout: float):
        self.conn: Client = conn
        self.timeout: float = timeout

    def get_action(self, s) -> int:
        # self.conn.settimeout(self.timeout)
        self.conn.send(('BattlePolicy', 'get_action', s))
        action: int = self.conn.recv()
        return action

    def requires_encode(self) -> bool:
        # self.conn.settimeout(ENCODE_TIMEOUT)
        self.conn.send(('BattlePolicy', 'requires_encode',))
        action: bool = self.conn.recv()
        return action

    def close(self):
        # self.conn.settimeout(CLOSE_TIMEOUT)
        self.conn.send(('BattlePolicy', 'close'))


class ProxySelectorPolicy(SelectorPolicy):

    def __init__(self, conn: Client, timeout: float):
        self.conn: Client = conn
        self.timeout: float = timeout

    def get_action(self, s) -> Set[int]:
        # self.conn.settimeout(self.timeout)
        self.conn.send(('SelectorPolicy', 'get_action', s))
        action: Set[int] = self.conn.recv()
        return action

    def requires_encode(self) -> bool:
        # self.conn.settimeout(ENCODE_TIMEOUT)
        self.conn.send(('SelectorPolicy', 'requires_encode',))
        action: bool = self.conn.recv()
        return action

    def close(self):
        # self.conn.settimeout(CLOSE_TIMEOUT)
        self.conn.send(('SelectorPolicy', 'close'))


class ProxyTeamBuilderPolicy(TeamBuilderPolicy):

    def __init__(self, conn: Client, timeout: float):
        self.conn: Client = conn
        self.timeout: float = timeout

    def get_action(self, s) -> PkmFullTeam:
        # self.conn.settimeout(self.timeout)
        self.conn.send(('TeamBuilderPolicy', 'get_action', s))
        action: PkmFullTeam = self.conn.recv()
        return action

    def requires_encode(self) -> bool:
        # self.conn.settimeout(ENCODE_TIMEOUT)
        self.conn.send(('TeamBuilderPolicy', 'requires_encode',))
        action: bool = self.conn.recv()
        return action

    def close(self):
        # self.conn.settimeout(CLOSE_TIMEOUT)
        self.conn.send(('TeamBuilderPolicy', 'close'))


class ProxyTeamPredictor(TeamPredictor):

    def __init__(self, conn: Client, timeout: float):
        self.conn: Client = conn
        self.timeout: float = timeout

    def get_action(self, s) -> PkmTeamPrediction:
        # self.conn.settimeout(self.timeout)
        self.conn.send(('TeamPredictor', 'get_action', s))
        action: PkmTeamPrediction = self.conn.recv()[0]
        return action

    def requires_encode(self) -> bool:
        # self.conn.settimeout(ENCODE_TIMEOUT)
        self.conn.send(('TeamPredictor', 'requires_encode',))
        action: bool = self.conn.recv()
        return action

    def close(self):
        # self.conn.settimeout(CLOSE_TIMEOUT)
        self.conn.send(('TeamPredictor', 'close'))


class ProxyDataAggregator(DataAggregator):

    def __init__(self, conn: Client, timeout: float):
        self.conn: Client = conn
        self.timeout: float = timeout

    def get_action(self, s) -> MetaData:
        # self.conn.settimeout(self.timeout)
        self.conn.send(('DataAggregator', 'get_action', s))
        action: MetaData = self.conn.recv()
        return action

    def requires_encode(self) -> bool:
        # self.conn.settimeout(ENCODE_TIMEOUT)
        self.conn.send(('DataAggregator', 'requires_encode',))
        action: bool = self.conn.recv()
        return action

    def close(self):
        # self.conn.settimeout(CLOSE_TIMEOUT)
        self.conn.send(('DataAggregator', 'close'))


class ProxyTeamValuator(TeamValuator):

    def __init__(self, conn: Client, timeout: float):
        self.conn: Client = conn
        self.timeout: float = timeout

    def get_action(self, s) -> TeamValue:
        # self.conn.settimeout(self.timeout)
        self.conn.send(('TeamValuator', 'get_action', s))
        action: TeamValue = self.conn.recv()
        return action

    def requires_encode(self) -> bool:
        # self.conn.settimeout(ENCODE_TIMEOUT)
        self.conn.send(('TeamValuator', 'requires_encode',))
        action: bool = self.conn.recv()
        return action

    def close(self):
        # self.conn.settimeout(CLOSE_TIMEOUT)
        self.conn.send(('BalancePolicy', 'close'))


class ProxyBalancePolicy(BalancePolicy):

    def __init__(self, conn: Client, timeout: float):
        self.conn: Client = conn
        self.timeout: float = timeout

    def get_action(self, s) -> PkmRoster:
        # self.conn.settimeout(self.timeout)
        self.conn.send(('BalancePolicy', 'get_action', s))
        action: PkmRoster = self.conn.recv()
        return action

    def requires_encode(self) -> bool:
        # self.conn.settimeout(ENCODE_TIMEOUT)
        self.conn.send(('BalancePolicy', 'requires_encode',))
        action: bool = self.conn.recv()
        return action

    def close(self):
        # self.conn.settimeout(CLOSE_TIMEOUT)
        self.conn.send(('BalancePolicy', 'close'))


GET_TEAM_TIMEOUT = 1.0
SET_TEAM_TIMEOUT = 1.0
META_DATA_TIMEOUT = 1.0
NAME_TIMEOUT = 1.0
RESET_TIMEOUT = 1.0
CHANGE_TEAM_TIMEOUT = 1.0


class ProxyCompetitor(Competitor):

    def __init__(self, conn: Client):
        self.conn = conn
        self.battlePolicy = ProxyBattlePolicy(conn, 1.0)
        self.selectorPolicy = ProxySelectorPolicy(conn, 1.0)
        self.teamBuilderPolicy = ProxyTeamBuilderPolicy(conn, 1.0)
        self.teamPredictor = ProxyTeamPredictor(conn, 1.0)
        self.dataAggregator = ProxyDataAggregator(conn, 1.0)
        self.teamValuator = ProxyTeamValuator(conn, 1.0)
        self.balancePolicy = ProxyBalancePolicy(conn, 1.0)

    @property
    def battle_policy(self) -> BattlePolicy:
        return self.battlePolicy

    @property
    def selector_policy(self) -> SelectorPolicy:
        return self.selectorPolicy

    @property
    def team_builder_policy(self) -> TeamBuilderPolicy:
        return self.teamBuilderPolicy

    @property
    def team_prediction_policy(self) -> TeamPredictor:
        return self.teamPredictor

    @property
    def data_aggregator_policy(self) -> DataAggregator:
        return self.dataAggregator

    @property
    def team_valuator_policy(self) -> TeamValuator:
        return self.teamValuator

    @property
    def balance_policy(self) -> BalancePolicy:
        return self.balancePolicy

    @property
    def team(self) -> PkmFullTeam:
        # self.conn.settimeout(GET_TEAM_TIMEOUT)
        self.conn.send(('get_team',))
        action: PkmFullTeam = self.conn.recv()
        return action

    @team.setter
    def team(self, team):
        # self.conn.settimeout(SET_TEAM_TIMEOUT)
        self.conn.send(('set_team', team))

    @property
    def meta_data(self) -> MetaData:
        # self.conn.settimeout(META_DATA_TIMEOUT)
        self.conn.send(('meta_data',))
        action: MetaData = self.conn.recv()
        return action

    @property
    def name(self) -> str:
        # self.conn.settimeout(NAME_TIMEOUT)
        self.conn.send(('name',))
        action: str = self.conn.recv()
        return action

    def reset(self):
        # self.conn.settimeout(RESET_TIMEOUT)
        self.conn.send(('reset',))

    @property
    def want_to_change_team(self) -> bool:
        # self.conn.settimeout(CHANGE_TEAM_TIMEOUT)
        self.conn.send(('want_to_change_team',))
        action: bool = self.conn.recv()
        return action
