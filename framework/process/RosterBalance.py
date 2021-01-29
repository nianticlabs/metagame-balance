from typing import Any

from framework.behaviour import BalancePolicy
from framework.DataObjects import MetaData, PkmRoster, DesignConstraints


class RosterBalance:

    def __init__(self, bp: BalancePolicy, meta_data: MetaData, roster: PkmRoster, constraints: DesignConstraints):
        self.__bp = bp
        self.__meta_data = meta_data
        self.__constraints = constraints
        self.__roster = roster

    def run(self) -> Any:
        try:
            self.__roster = self.__bp.get_action((self.__meta_data, self.__roster, self.__constraints))
        except:
            pass

    @property
    def roster(self):
        return self.__roster
