import dataclasses

import numpy as np

from metagame_balance.framework import GameEnvironment, StateDelta, G, EvaluationResult, State


@dataclasses.dataclass
class CoolGameState(State["CoolGameEnvironment"]):
    torch_health: int = 1
    torch_dmg: int = 1
    torch_torch_range: int = 1
    torch_duration: int = 1
    torch_cooldown: int = 1
    torch_ticks_between_moves: int = 1

    saw_health: int = 1
    saw_dmg_min: int = 1
    saw_dmg_max: int = 1
    saw_duration: int = 1
    saw_cooldown: int = 1
    saw_ticks_between_moves: int = 1

    nail_health: int = 1
    nail_dmg: int = 1
    nail_cooldown: int = 1
    nail_ticks_between_moves: int = 1

    def encode(self) -> np.array:
        return np.array([
            self.torch_health,  # index 0
            self.torch_dmg,
            self.torch_torch_range,
            self.torch_duration,
            self.torch_cooldown,
            self.torch_ticks_between_moves,

            self.saw_health,
            self.saw_dmg_min,
            self.saw_dmg_max,
            self.saw_duration,
            self.saw_cooldown,
            self.saw_ticks_between_moves,

            self.nail_health,
            self.nail_dmg,
            self.nail_cooldown,
            self.nail_ticks_between_moves  # index 15
        ])

    @classmethod
    def decode(cls, encoded: np.array) -> "CoolGameState":
        return cls(
            encoded[0],
            encoded[1],
            encoded[2],
            encoded[3],
            encoded[4],
            encoded[5],
            encoded[6],
            encoded[7],
            encoded[8],
            encoded[9],
            encoded[10],
            encoded[11],
            encoded[12],
            encoded[13],
            encoded[14],
            encoded[15]
        )


@dataclasses.dataclass
class CoolGameStateDelta(StateDelta["CoolGameEnvironment"]):
    next_state: CoolGameState

    @classmethod
    def decode(cls, encoded_next_state: np.ndarray, current_state: CoolGameState) -> "CoolGameStateDelta":
        return cls(CoolGameState.decode(encoded_next_state))


@dataclasses.dataclass
class CoolGameEvaluationResult(EvaluationResult["CoolGameEnvironment"]):
    entropy: float

    def encode(self) -> float:
        return self.entropy


class CoolGameEnvironment(GameEnvironment):
    def __init__(self):
        self.current_state = CoolGameState()

    def evaluate(self) -> EvaluationResult[G]:
        pass

    def get_state(self) -> CoolGameState:
        return self.current_state

    def reset(self) -> CoolGameState:
        pass

    def get_state_bounds(self):
        pass

    def apply(self, state_delta: StateDelta[G]) -> \
            "State[G]":
        pass

    def __str__(self) -> str:
        return "CoolGameEnvironment"

    def snapshot_gameplay_policies(self, path: str):
        pass

    def snapshot_game_state(self, path: str):
        pass

    def plot_rewards(self, path: str):
        pass
