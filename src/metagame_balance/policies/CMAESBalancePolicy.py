from typing import Tuple, Callable, Optional

import cma
import numpy as np

from metagame_balance.framework import MetagameBalancePolicy, State, G, StateDelta, EvaluationResult
from metagame_balance.vgc.balance import DeltaRoster
from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.balance.restriction import DesignConstraints
from metagame_balance.vgc.behaviour import BalancePolicy
from metagame_balance.vgc.datatypes.Objects import PkmRoster
from metagame_balance.vgc.util.RosterParsers import MetaRosterStateParser


class CMAESBalancePolicyV2(MetagameBalancePolicy):
    def __init__(self, init_var = 0.05): #low var for faster convergence near the initial solution
        super().__init__()
        self.results = {
            'x': [],
            'y': []
        }
        self.generation_samples = []
        self.optimizer = None
        self.num_runs = 0
        self.init_var = init_var

    def get_suggestion(self, environment: G, state: State[G],
                       state_delta_constructor: Callable[[np.ndarray, State[G]], StateDelta[G]],
                       evaluation_result: EvaluationResult[G]) -> StateDelta[G]:
        x = state.encode()
        y = evaluation_result.encode()

        self.results['x'].append(x)
        self.results['y'].append(y)

        if len(self.generation_samples) == 0:
            if self.optimizer is not None:
                self.optimizer.tell(self.results['x'], self.results['y'])
            else:
                bounds = environment.get_state_bounds()
                self.optimizer = cma.CMAEvolutionStrategy(x, self.init_var,
                        {'bounds': bounds}) #'popsize':30})
            self.generation_samples = self.optimizer.ask()
            self.results = {'x': [], 'y': []}
        next_state = self.generation_samples.pop(0)
        self.num_runs += 1
        return state_delta_constructor(next_state, state)

    def converged(self, evaluation_result: Optional[EvaluationResult[G]]) -> bool:
        return False


class CMAESBalancePolicy(BalancePolicy):
    """
    """

    def __init__(self, num_pkm):

        self.parser = MetaRosterStateParser(num_pkm)
        self.num_pkm = num_pkm
        self.optimizer = None
        self.generation_samples = []
        self.results = {'x' : [], 'y' : []}

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> DeltaRoster:
        """
        Look at meta data, give it to CMA-ES and return value
        """
        meta_data = d[1]

        state = self.parser.metadata_to_state(meta_data)

        y = meta_data.evaluate()
        self.results['x'].append(state)
        self.results['y'].append(y)
        if len(self.generation_samples) == 0:
            if self.optimizer is not None:
                self.optimizer.tell(self.results['x'], self.results['y'])
            else:
                bounds = self.parser.get_state_bounds()
                self.optimizer = cma.CMAEvolutionStrategy(state, 0.05, {'bounds': bounds})
            self.generation_samples = self.optimizer.ask()
            self.results = {'x' : [], 'y' : []}
        next_state = self.generation_samples.pop(0)
        return self.parser.state_to_delta_roster(next_state, meta_data)

    @property
    def stop(self) -> bool:
        """
        TODO: use this in main loop for early stopping/ testing convergence
        """
        return False if self.optimizer is None else self.optimizer.stop()
