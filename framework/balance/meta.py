from abc import ABC
from typing import Set, Dict, Tuple, List

from framework.balance.archtype import TeamArchtype
from framework.datatypes.Objects import PkmTemplate


class MetaData(ABC):
    pass


class StandardMetaData(MetaData):

    def __init__(self, _max_history_size: int = 1e5, unlimited: bool = False):
        self._teams: Set[TeamArchtype] = set()
        self._victories: Dict[Tuple[TeamArchtype, TeamArchtype], int] = {}
        self._usage: Dict[TeamArchtype, int] = {}
        self._pkm_usage: Dict[PkmTemplate, int] = {}
        self._history: List[TeamArchtype] = []
        self._pkm_history: List[PkmTemplate] = []
        self._max_history_size: int = _max_history_size * 2
        self._total_usage = 0
        self._total_pkm_usage = 0
        self._unlimited = unlimited

    def set_archtype(self, archtype: TeamArchtype):
        if archtype not in self._teams:
            for existing in self._teams:
                self._victories[(archtype, existing)] = 0
                self._victories[(existing, archtype)] = 0
            self._usage[archtype] = 0
            self._teams.add(archtype)

    def update(self, winner: TeamArchtype, loser: TeamArchtype):
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
                self._remove_archtype(old_achtype0)
            if self._usage[old_achtype1] == 0:
                self._remove_archtype(old_achtype1)

    def _remove_archtype(self, archtype: TeamArchtype):
        self._teams.remove(archtype)
        self._usage.pop(archtype)
        for existing in self._teams:
            self._victories.pop((archtype, existing))
            self._victories.pop((existing, archtype))

    def get_winrate(self, archtype: TeamArchtype, opponent: TeamArchtype) -> float:
        if archtype == opponent:
            return 0.5
        victories = self._victories[(archtype, opponent)]
        losses = self._victories[(opponent, archtype)]
        return victories / max((victories + losses), 1)

    def get_usagerate(self, archtype: TeamArchtype):
        return self._usage[archtype] / self._total_usage

    def get_pkm_usagerate(self, pkm: PkmTemplate):
        return self._pkm_usage[pkm] / self._total_pkm_usage
