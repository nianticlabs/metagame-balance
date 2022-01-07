from typing import Any

from framework.balance.meta import MetaData
from framework.balance.restriction import DesignConstraints
from framework.behaviour import BalancePolicy
from framework.datatypes.Objects import PkmRoster


class RosterBalance:

    def __init__(self, bp: BalancePolicy, meta_data: MetaData, roster: PkmRoster, constraints: DesignConstraints):
        self.bp = bp
        self.meta_data = meta_data
        self.onstraints = constraints
        self.roster = roster

    # noinspection PyBroadException
    def run(self) -> Any:
        roster = self.roster
        try:
            self.roster = self.bp.get_action((self.meta_data, self.roster, self.onstraints))
        except:
            pass
        if self.roster != roster:
            roster = self.roster
        return roster
