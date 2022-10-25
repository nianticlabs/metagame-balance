import dataclasses
import json
import logging
import typing
from pathlib import Path

from tqdm.auto import  tqdm

import gym
# this registers the gym on import, don't comment out this line
import gym_cool_game  # noqa
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from regym.environments import EnvType
from regym.environments.gym_parser import parse_gym_environment
from regym.evaluation import benchmark_agents_on_tasks
from regym.rl_algorithms import build_MCTS_Agent
from scipy.special import softmax
from scipy.stats import entropy

from metagame_balance.BalanceMeta import plot_rewards
from metagame_balance.Tabular_Function import TabularFn
from metagame_balance.cool_game import BotType
from metagame_balance.framework import GameEnvironment, StateDelta, EvaluationResult, State
from metagame_balance.rpsfw.SoftmaxCompetitor import SoftmaxCompetitor
from metagame_balance.utility import UtilityFunctionManager

# these aren't technically bounded in any way, but we'll practically bound them like this
STATE_BOUNDS = [1, 10]

MCTS_BUDGET = 625  # section 6.C
MCTS_BUDGET = 5  # section 6.C
BENCHMARKING_EPISODES = 50  # section 6.B
ROLLOUT_BUDGET = 100 # various places in GGJ repo

DEFAULT_MCTS_CONFIG = {"budget": MCTS_BUDGET,
                       'rollout_budget': ROLLOUT_BUDGET,
                       # these two are in the GGJ-cool-game repo
                       "selection_phase": "ucb1",
                       "exploration_factor_ucb1": 4}


@dataclasses.dataclass
class CoolGameState(State["CoolGameEnvironment"]):

    torch_health: int = 7
    torch_dmg: int = 3
    torch_torch_range: int = 3
    torch_duration: int = 2
    torch_cooldown: int = 5
    torch_ticks_between_moves: int = 4

    saw_health: int = 4
    saw_dmg_min: int = 6
    saw_dmg_max: int = 8
    saw_duration: int = 3
    saw_cooldown: int = 3
    saw_ticks_between_moves: int = 5

    nail_health: int = 3
    nail_dmg: int = 9
    nail_cooldown: int = 1
    nail_ticks_between_moves: int = 2
    """
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

    nail_health: int = 6
    nail_dmg: int = 6
    nail_cooldown: int = 6
    nail_ticks_between_moves: int = 6
    """

    @classmethod
    def random(cls):
        """
        Generate randomly initialized (random int in range) state vector.

        In practice, it is bad to use this because it makes early episodes take a long time.
        """
        return cls(*np.random.randint(STATE_BOUNDS[0], STATE_BOUNDS[1], size=len(dataclasses.fields(cls))))

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
            int(encoded[0]),
            int(encoded[1]),
            int(encoded[2]),
            int(encoded[3]),
            int(encoded[4]),
            int(encoded[5]),
            int(encoded[6]),
            int(encoded[7]),
            int(encoded[8]),
            int(encoded[9]),
            int(encoded[10]),
            int(encoded[11]),
            int(encoded[12]),
            int(encoded[13]),
            int(encoded[14]),
            int(encoded[15])
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
    for i in tqdm(range(benchmarking_episodes), desc="erg benchmark"):
        logging.info(f'Budget: {mcts_budget}. {matchup} episode: {i + 1}/{benchmarking_episodes}')
        winrates += benchmark_agents_on_tasks(tasks=[task],
                                              agents=[agent],
                                              populate_all_agents=True,
                                              num_episodes=1)
    winrate = sum(winrates) / len(winrates)

    return winrate


def _make_gym(botA_type, botB_type, **kwargs):
    initial_env = gym.make("CoolGame-v0", botA_type=botA_type, botB_type=botB_type, **kwargs)
    # no wrappers
    return parse_gym_environment(initial_env, EnvType.MULTIAGENT_SIMULTANEOUS_ACTION)


class CoolGameEnvironment(GameEnvironment):
    @property
    def last_encoded_gamestate_path(self) -> str:
        return ""

    @property
    def latest_gamestate_path(self) -> str:
        return str(self._latest_gamestate_path)

    @property
    def latest_agent_policy_path(self) -> str:
        return ""

    @property
    def latest_adversary_policy_path(self) -> str:
        return ""

    @property
    def latest_entropy_path(self) -> str:
        return ""

    def __init__(self, epochs: int, reg_param: int = 0,
                 alg_baseline: bool = False):
        self.alg_baseline = alg_baseline
        self.epochs = epochs
        self.reg = reg_param
        fn_approx = TabularFn(3)
        self.utility_manager = UtilityFunctionManager(fn_approx, delay_by=10)
        # random initialization tends to create envs that are very slow to evaluate
        # instead, use the defaults specified in the paper
        self.current_state: CoolGameState = CoolGameState()
        self.item_reverse_map = {'saw': 0, 'torch': 1, 'nail': 2}
        self.item_map = ['saw', 'torch', 'nail']
        self.rewards: typing.List[float] = []
        self.entropy: typing.List[float] = []
        self.players = [SoftmaxCompetitor("agent", TabularFn(3), True),
                        SoftmaxCompetitor("adversary", TabularFn(3), True)]
        # TODO maybe don't hardcode these
        self.saw_vs_nail_tgt = 0.5
        self.torch_vs_nail_tgt = 0.5
        self.saw_vs_torch_tgt = 0.5

        self.num_samples = 0
        self._latest_gamestate_path: typing.Optional[Path] = None

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


        # we will learn the agent once and never update it, like how the other environments work
        mcts_agent = build_MCTS_Agent(saw_vs_torch_task, DEFAULT_MCTS_CONFIG, "mcts agent")
        saw_vs_torch = compute_matchup_winrates(mcts_agent, saw_vs_torch_task,
                                                'Saw vs Torch', BENCHMARKING_EPISODES,
                                                MCTS_BUDGET)

        saw_vs_nail = compute_matchup_winrates(mcts_agent, saw_vs_nail_task,
                                               'Saw vs Nail', BENCHMARKING_EPISODES,
                                               MCTS_BUDGET)

        torch_vs_nail = compute_matchup_winrates(mcts_agent, torch_vs_nail_task,
                                                 'Torch vs Nail', BENCHMARKING_EPISODES,
                                                 MCTS_BUDGET)
        logging.info(f"episodes={BENCHMARKING_EPISODES} mcts_budget={MCTS_BUDGET}")
        logging.info(f'winrates=saw vs torch:{saw_vs_torch} saw vs nail {saw_vs_nail} torch:[{torch_vs_nail}]')
        logging.info(f'params={self.current_state}')

        winrates = np.array([saw_vs_nail, torch_vs_nail, saw_vs_torch])
        reward = ((winrates - self.target_erg_arr()) ** 2).sum()
        """
        ERG will be (winrate saw_vs_nail - ideal)^2  + (win_rate torch_vs_nail)^2 + ...
        """
        logging.info("ERG=%s", reward)
        self.rewards.append(reward)
        self.evaluate_entropy(eval_only=True)  ### Just for logging!
        return CoolGameEvaluationResult(reward)

    def target_erg_arr(self):
        # saw, torch, nail
        # flattened repr of erg for erg difference calculation
        return np.array([self.saw_vs_nail_tgt, self.torch_vs_nail_tgt, self.saw_vs_torch_tgt])

    def evaluate(self) -> CoolGameEvaluationResult:
        if self.alg_baseline:
            return self.evaluate_ERG()
        return self.evaluate_entropy()

    def evaluate_entropy(self, eval_only=False):
        for i in range(self.epochs):
            item1, item2 = self.players[0].get_action(self.item_map), \
                           self.players[1].get_action(self.item_map)
            items = [item1, item2]
            if item1 == item2:
                reward = 0
            else:
                env = _make_gym(botA_type=item1, botB_type=item2,
                                **dataclasses.asdict(self.current_state))
                mcts_agent = build_MCTS_Agent(env, DEFAULT_MCTS_CONFIG, "mcts agent")

                # reward is 1 if item1 wins, 0 if item2 wins
                reward = compute_matchup_winrates(
                    mcts_agent, env,
                    'botA_botB', 1,  # instead of benchmarking 1000 times, we sample once
                    MCTS_BUDGET)
                reward = (reward * 2) - 1
                self.num_samples+=1
            logging.info("P1: %s: P2: %s won:%s", item1, item2, reward)
            for player_i, player in enumerate(self.players):
                # player internally flips reward for opponent
                player.update(items[player_i], reward)

        u = self.players[0].get_u_fn().get_all_vals()
        P_A = softmax(u)
        logging.info("P_A = %s", str(P_A))
        print(P_A)
        entropy_loss = -entropy(P_A)
        self.entropy.append(entropy_loss)
        logging.info("Entropy Loss=%s", entropy_loss)
        if not eval_only:
            self.rewards.append(entropy_loss)
            return CoolGameEvaluationResult(entropy_loss)
        else:
            return entropy_loss

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
        import os
        logging.info("Objective: %s \n", str(self.rewards))
        logging.info("Entropy_loss: %s \n", str(self.entropy))
        logging.info("Num Samples: %s \n", str(self.num_samples))
        gamestate_path = Path(path) / "game_state.json"
        with gamestate_path.open("w") as outfile:
            json.dump(dataclasses.asdict(self.current_state), outfile)
        np.save(os.path.join(path, "entropies.npy"), np.array(self.entropy))
        self._latest_gamestate_path = gamestate_path

    def plot_rewards(self, path: str):
        print(self.rewards)
        plot_rewards(self.rewards)
        plt.savefig(path)
