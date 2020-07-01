from Engine.PkmConstants import MAX_TEAM_SIZE, DEFAULT_SELECTION_SIZE
from Trainer.Tabular.Abstract.Agent import *
import random


class RandomSelectionAgent(SelectionAgent):

    def __init__(self, teams_size: int = MAX_TEAM_SIZE, selection_size: int = DEFAULT_SELECTION_SIZE):
        self.teams_size = teams_size
        self.selection_size = selection_size

    def get_action(self, s) -> List[int]:
        return random.shuffle([i for i in range(self.teams_size)])[:self.selection_size]

    def close(self):
        pass
