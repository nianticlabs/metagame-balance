import itertools
from abc import ABC, abstractmethod
from math import exp
from typing import Dict, Tuple, List
import copy
from scipy.stats import entropy
from copy import deepcopy
#from vgc.util.RosterParsers import MetaRosterStateParser
from vgc.balance import DeltaRoster
from vgc.balance.archtype import std_move_dist, std_pkm_dist, std_team_dist
from vgc.datatypes.Objects import PkmTemplate, PkmMove, PkmFullTeam, PkmRoster
from vgc.balance.meta import MetaData, PkmId
from vgc.util.RosterParsers import MetaRosterStateParser


class WinrateEntropyMetaData(MetaData):

    def __init__(self):
        # listings - moves, pkm, teams
        self._moves: List[PkmMove] = []
        self._pkm: List[PkmTemplate] = []

        self._pkm_wins: Dict[PkmId, int] = {}

    def set_moves_and_pkm(self, roster: PkmRoster):
        self._pkm = list(roster)
        self._moves = []
        for pkm in self._pkm:
            self._moves += list(pkm.move_roster)

        init_metadata = copy.deepcopy(self)
        self.parser = MetaRosterStateParser(len(self._pkm))
        self.init_state = self.parser.metadata_to_state(init_metadata)


    def clear_stats(self):
        for pkm in self._pkm:
            self._pkm_wins[pkm.pkm_id] = 0

    def update_with_delta_roster(self, delta: DeltaRoster):
        return

    def update_metadata(self, **kwargs):

        self.update_with_delta_roster(kwargs['delta'])
        #stage 2 policy
        #delta roster

    def update_with_policy(self, policy):
        raise NotImplementedError

    def update_with_team(self, team: PkmFullTeam, won: bool):

        for pkm in team.pkm_list:
            if won:
                self._pkm_wins[pkm.pkm_id] += 1
        """
        update the meta with team if required in future
        """

    def distance_from_init_meta(self):

        state = self.parser.metadata_to_state(self)

        return ((state - self.init_state) ** 2).mean(axis=0) / 100 ##something reasonable


    def evaluate(self, distance_loss = False) -> float:
        loss = -entropy([x / sum(self._pkm_wins.values())  for x in self._pkm_wins.values()])
        if distance_loss:
            return loss + self.distance_from_init_meta()
        return loss
