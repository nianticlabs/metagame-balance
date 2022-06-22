from vgc.behaviour import BalancePolicy
from vgc.balance import DeltaRoster, DeltaPkm
from vgc.balance.meta import MetaData
from vgc.balance.restriction import DesignConstraints
from vgc.behaviour import BalancePolicy
from vgc.datatypes.Objects import PkmRoster
from vgc.util.RosterParsers import MetaRosterStateParser
from typing import Tuple
import copy
import cma
import numpy as np
class CMAESBalancePolicy(BalancePolicy):

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
                self.optimizer = cma.CMAEvolutionStrategy(state, 20, {'bounds': [np.zeros((len(state))), None]})
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
