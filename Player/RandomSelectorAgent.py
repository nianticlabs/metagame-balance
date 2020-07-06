from typing import List

from Engine.PkmConstants import MAX_TEAM_SIZE, DEFAULT_SELECTION_SIZE
import random

from Player.Abstract.Agent import SelectorAgent


class RandomSelectorAgent(SelectorAgent):

    def __init__(self, teams_size: int = MAX_TEAM_SIZE, selection_size: int = DEFAULT_SELECTION_SIZE):
        self.teams_size = teams_size
        self.selection_size = selection_size

    def get_action(self, s) -> List[int]:
        ids = [i for i in range(self.teams_size)]
        random.shuffle(ids)
        return ids[:self.selection_size]

    def close(self):
        pass
