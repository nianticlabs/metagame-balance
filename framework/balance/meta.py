from abc import ABC
from typing import Set, Dict, Tuple, List

from framework.balance.archtype import Archtype


class MetaData(ABC):
    pass


class StandardMetaData(MetaData):

    def __init__(self, _max_history_size: int = 1e5, unlimited: bool = False):
        self._teams: Set[Archtype] = set()
        self._victories: Dict[Tuple[Archtype, Archtype], int] = {}
        self._usage: Dict[Archtype, int] = {}
        self._history: List[Archtype] = []
        self._max_history_size: int = _max_history_size * 2
        self._total_usage = 0
        self._unlimited = unlimited

    def set_archtype(self, archtype: Archtype):
        if archtype not in self._teams:
            for existing in self._teams:
                self._victories[(archtype, existing)] = 0
                self._victories[(existing, archtype)] = 0
            self._usage[archtype] = 0
            self._teams.add(archtype)

    def update(self, winner: Archtype, loser: Archtype):
        self._victories[(winner, loser)] += 1
        self._usage[winner] += 1
        self._usage[loser] += 1
        self._total_usage += 2
        self._history.append(winner)
        self._history.append(loser)
        if len(self._history) > self._max_history_size and not self._unlimited:
            old_achtype0 = self._history.pop(0)
            old_achtype1 = self._history.pop(0)
            self._usage[old_achtype0] -= 1
            self._usage[old_achtype1] -= 1
            self._total_usage -= 2
            if self._usage[old_achtype0] == 0:
                self.remove_archtype(old_achtype0)
            if self._usage[old_achtype1] == 0:
                self.remove_archtype(old_achtype1)

    def remove_archtype(self, archtype: Archtype):
        self._teams.remove(archtype)
        self._usage.pop(archtype)
        for existing in self._teams:
            self._victories.pop((archtype, existing))
            self._victories.pop((existing, archtype))

    def get_winrate(self, archtype: Archtype, opponent: Archtype) -> float:
        if archtype == opponent:
            return 0.5
        victories = self._victories[(archtype, opponent)]
        losses = self._victories[(opponent, archtype)]
        return victories / max((victories + losses), 1)

    def get_usagerate(self, archtype: Archtype):
        return self._usage[archtype] / self._total_usage
