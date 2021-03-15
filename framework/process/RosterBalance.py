from typing import Any

from framework.DataObjects import MetaData, PkmRoster, DesignConstraints
from framework.behaviour import BalancePolicy


class RosterBalance:

    def __init__(self, bp: BalancePolicy, meta_data: MetaData, roster: PkmRoster, constraints: DesignConstraints):
        self.__bp = bp
        self.__meta_data = meta_data
        self.__constraints = constraints
        self.__roster = roster

    # noinspection PyBroadException
    def run(self) -> Any:
        roster = self.__roster
        try:
            self.__roster = self.__bp.get_action((self.__meta_data, self.__roster, self.__constraints))
        except:
            pass
        if self.__roster != roster:
            roster = self.__roster
        return roster

    @property
    def roster(self):
        return self.__roster
