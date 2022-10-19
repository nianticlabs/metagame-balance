from typing import Sized

from metagame_balance.rpsfw.util import MetaData


class RPSFWRoster(Sized):
    def __len__(self) -> int:
        return len(self.roster_win_probs)

    def __init__(self, metadata: MetaData):
        self.roster_win_probs = metadata.get_win_probs()

    def update_win_probs(self, win_probs):
        for i in range(len(win_probs)):
            for j in range(len(win_probs[0])):
                self.roster_win_probs[i][j] = win_probs[i][j]


class RPSFWDeltaRoster:
    def __init__(self, win_probs):
        self.roster_win_probs = win_probs

    def apply(self, roster: RPSFWRoster):
        roster.update_win_probs(self.roster_win_probs)
