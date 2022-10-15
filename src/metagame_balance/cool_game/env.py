import dataclasses
import logging
import time
import typing

import gym
# this registers the gym on import, don't delete
import gym_cool_game  # noqa
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from regym.environments import EnvType
from regym.environments.gym_parser import parse_gym_environment
from regym.evaluation import benchmark_agents_on_tasks
from regym.rl_algorithms import build_MCTS_Agent
from scipy.stats import entropy

from metagame_balance.BalanceMeta import plot_rewards
from metagame_balance.cool_game import BotType
from metagame_balance.framework import GameEnvironment, StateDelta, EvaluationResult, State

# these aren't technically bounded in any way, but we'll practically bound them like this
STATE_BOUNDS = [1, 1000]


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

    def encode(self) -> npt.NDArray:
        # the optimizer wants all of these in [0, 1]
        return ((np.array([
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
        ]) - STATE_BOUNDS[0]) / (STATE_BOUNDS[1] - STATE_BOUNDS[0]))

    @classmethod
    def decode(cls, encoded: npt.NDArray) -> State["CoolGameEnvironment"]:
        encoded = (encoded * (STATE_BOUNDS[1] - STATE_BOUNDS[0]) + STATE_BOUNDS[0]).round().astype(int)
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
        # logging.info(f'{matchup} with Budget: {mcts_budget} took {total:.1f}s. Winner: {winrates[-1]}')
    winrate = sum(winrates) / len(winrates)
    # logging.info(f'END: {matchup} for {benchmarking_episodes} episodes. winrate: {winrate}')

    return winrate


def _make_gym(botA_type, botB_type, **kwargs):
    initial_env = gym.make("CoolGame-v0", botA_type=botA_type, botB_type=botB_type, **kwargs)
    # no wrappers
    return parse_gym_environment(initial_env, EnvType.MULTIAGENT_SIMULTANEOUS_ACTION)


class CoolGameEnvironment(GameEnvironment):
    def __init__(self, epochs: int, reg_param: int = 0,
            alg_baseline: bool= False, relearn_agents: bool = False):
        """

        Parameters
        ----------
        relearn_agents: relearn the agents on every evaluation call or not.
        """
        self.alg_baseline = alg_baseline
        self.epochs = epochs
        self.reg = reg_param
        self.current_state: CoolGameState = CoolGameState()
        self.rewards: typing.List[float] = []

    def evaluate_ERG(self) -> CoolGameEvaluationResult:
        # from https://github.com/Danielhp95/GGJ-2020-cool-game/blob/master/hyperopt_mongo/cool_game_regym_hyperopt.py
        # 0 - sawbot, 1 - torchbot, 2 - nailbot
        # regym framework got mildly broken, so use my weird version
        saw_vs_torch_task = _make_gym(botA_type=BotType.SAW, botB_type=BotType.TORCH,
                                      **dataclasses.asdict(self.current_state))
        # saw_vs_nail_task = generate_task("CoolGame-v0", EnvType.MULTIAGENT_SIMULTANEOUS_ACTION,
        saw_vs_nail_task = _make_gym(botA_type=BotType.SAW, botB_type=BotType.NAIL,
                                     **dataclasses.asdict(self.current_state))
        torch_vs_nail_task = _make_gym(botA_type=BotType.TORCH, botB_type=BotType.NAIL,
                                       **dataclasses.asdict(self.current_state))
        # TODO don't hardcode
        mcts_budget = 5
        benchmarking_episodes = 10
        mcts_config = {"budget": mcts_budget, 'rollout_budget': 10,
                       "selection_phase": "ucb1", "exploration_factor_ucb1": 4}
        # we will learn the agent once and never update it, like how the other environments work
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


        reward = self.entropy_from_winrates([saw_vs_torch, saw_vs_nail, torch_vs_nail])
        self.rewards.append(reward)
        return CoolGameEvaluationResult(reward)

    def evaluate(self) -> CoolGameEvaluationResult:
        if self.alg_baseline:
            return self.evaluate_ERG()
        return self.evaluate_entropy()

    def evaluate_entropy(self):

    def get_state(self) -> State["CoolGameEnvironment"]:
        return self.current_state

    def reset(self) -> CoolGameState:
        # evaluation is a pure function, no mutable state in this object to reset
        pass

    def get_state_bounds(self):
        return [0, 1]

    def apply(self, state_delta: CoolGameStateDelta) -> CoolGameState:
        self.current_state = state_delta.next_state
        return state_delta.next_state

    def __str__(self) -> str:
        return "CoolGameEnvironment"

    def snapshot_gameplay_policies(self, path: str):
        pass

    def snapshot_game_state(self, path: str):
        pass

    def plot_rewards(self, path: str):
        plot_rewards(self.rewards)
        plt.savefig(path)
