import dataclasses
import logging
import time

import numpy as np
import numpy.typing as npt
from regym.evaluation import benchmark_agents_on_tasks
from regym.rl_algorithms import build_MCTS_Agent

from metagame_balance.framework import GameEnvironment, StateDelta, G, EvaluationResult, State
from regym.environments import generate_task, EnvType


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

    def to_dict(self):
        """Convert to format compatible with evaluator"""
        raise NotImplementedError

    def encode(self) -> npt.NDArray:
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
    def decode(cls, encoded: npt.NDArray) -> State["CoolGameEnvironment"]:
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
    next_state: State["CoolGameEnvironment"]

    @classmethod
    def decode(cls, encoded_next_state: npt.NDArray, current_state: State["CoolGameEnvironment"]) \
            -> "CoolGameStateDelta":
        return cls(CoolGameState.decode(encoded_next_state))


@dataclasses.dataclass
class CoolGameEvaluationResult(EvaluationResult["CoolGameEnvironment"]):
    entropy: float

    def encode(self) -> float:
        return self.entropy


def compute_matchup_winrates(agent, task, matchup: str,
                             benchmarking_episodes: int, mcts_budget: int) -> float:

    logging.info(f'START: {matchup} for {benchmarking_episodes} episodes. Budget: {mcts_budget}')
    winrates = []
    for i in range(benchmarking_episodes):
        logging.info(f'Budget: {mcts_budget}. {matchup} episode: {i + 1}/{benchmarking_episodes}')
        start = time.perf_counter()
        winrates += benchmark_agents_on_tasks(tasks=[task],
                                              agents=[agent],
                                              populate_all_agents=True,
                                              num_episodes=1)
        total = time.perf_counter() - start
        logging.info(f'{matchup} with Budget: {mcts_budget} took {total:.1f}s. Winner: {winrates[-1]}')
    winrate = sum(winrates) / len(winrates)
    logging.info(f'END: {matchup} for {benchmarking_episodes} episodes. winrate: {winrate}')

    return winrate


class CoolGameEnvironment(GameEnvironment):
    def __init__(self):
        self.current_state: CoolGameState = CoolGameState()

    def evaluate(self) -> CoolGameEvaluationResult:
        # from https://github.com/Danielhp95/GGJ-2020-cool-game/blob/master/hyperopt_mongo/cool_game_regym_hyperopt.py
        # 0 - sawbot, 1 - torchbot, 2 - nailbot
        saw_vs_torch_task = generate_task('CoolGame-v0', EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                          botA_type=0, botB_type=1, **self.current_state.to_dict())
        saw_vs_nail_task = generate_task("CoolGame-v0", EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                         botaA_type=0, botB_type=2, **self.current_state.to_dict())
        torch_vs_nail_task = generate_task("CoolGame-V0", EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
                                           botA_type=1, botB_type=2, **self.current_state.to_dict())
        # TODO not fixed
        mcts_budget = 5
        benchmarking_episodes = 10
        mcts_config = {"budget": mcts_budget, 'rollout_budget': 10}
        # agent is shared since it doesn't learn
        mcts_agent = build_MCTS_Agent(saw_vs_torch_task, mcts_config, "mcts agent")
        saw_vs_torch = compute_matchup_winrates(mcts_agent, saw_vs_torch_task,
                                                'Saw vs Torch', benchmarking_episodes,
                                                mcts_budget)

        saw_vs_nail = compute_matchup_winrates(mcts_agent, saw_vs_nail_task,
                                               'Saw vs Nail', benchmarking_episodes,
                                               mcts_budget)

        torch_vs_nail = compute_matchup_winrates(mcts_agent, torch_vs_nail_task,
                                                 'Torch vs Nail', benchmarking_episodes,
                                                 mcts_budget)
        logging.info(f"episodes={benchmarking_episodes} mcts_budget={mcts_budget}")
        logging.info(f'winrates=saw:[{saw_vs_torch}, {saw_vs_nail}] torch:[{torch_vs_nail}]')
        logging.info(f'params={self.current_state}')

        return CoolGameEvaluationResult(self.entropy_from_winrates([saw_vs_torch, saw_vs_nail, torch_vs_nail]))

    def entropy_from_winrates(self, winrates) -> float:
        """compute pick entropy from winrates"""
        # we have 3 types of robot, we assume the 

        raise NotImplementedError

    def get_state(self) -> State["CoolGameEnvironment"]:
        return self.current_state

    def reset(self) -> CoolGameState:
        pass

    def get_state_bounds(self):
        pass

    def apply(self, state_delta: StateDelta["CoolGameEnvironment"]) -> \
            "State[CoolGameEnvironment]":
        pass

    def __str__(self) -> str:
        return "CoolGameEnvironment"

    def snapshot_gameplay_policies(self, path: str):
        pass

    def snapshot_game_state(self, path: str):
        pass

    def plot_rewards(self, path: str):
        pass
