from copy import deepcopy
from typing import Any

from framework.behaviour import BalancePolicy
from framework.DataObjects import MetaData, PkmRoster


class RosterBalance:

    def __init__(self, bp: BalancePolicy, meta_data: MetaData, roster: PkmRoster):
        self.bp = bp
        self.meta_data = meta_data
        self.roster = roster

    def get_roster(self) -> Any:
        meta_data = deepcopy(self.meta_data)
        roster = deepcopy(self.roster)
        try:
            roster = self.bp.get_action((meta_data, roster))
        except:
            return self.roster
        return roster
