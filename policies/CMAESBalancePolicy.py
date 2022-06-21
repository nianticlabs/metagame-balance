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
       
        """
        DEBUGGING HELPERS  
        self.init_state = None
        self.call_ctr = 0 
        self.init_meta = None
        """
    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> DeltaRoster:
        
        """
        state vector [move_id_1_feat_1, move_id_1_feat_2, .. move_id_2_feat1, .... pkm_1_feat_1, pkm_1_feat_2, ..]
        """
        meta_data = d[1]

        """
        if self.init_state is None:
            self.init_state = self.parser.metadata_to_state(meta_data)
        import random
        if random.random() < 0.04:
            print("random choice")
            return self.parser.state_to_delta_roster(self.init_state, meta_data)

        """
        state = self.parser.metadata_to_state(meta_data)
        """
        if self.optimizer == None:
            for pkm in (d[0]):
                print(pkm)
                for move in pkm.move_roster:
                    print(move, move.power, move.acc, move.max_pp)
        self.init_meta = meta_data if self.init_state is None else self.init_meta
        self.init_state = state if self.init_state is None else self.init_state
        if self.call_ctr > 5:
            for pkm in (d[0]):
                print(pkm)
                for move in pkm.move_roster:
                    print(move, move.power, move.acc, move.max_pp)
            return self.parser.state_to_delta_roster(self.init_state, self.init_meta)
        """
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
        #self.call_ctr += 1
        return self.parser.state_to_delta_roster(next_state, meta_data)

    @property
    def stop(self) -> bool:
        
        return False if self.optimizer is None else self.optimizer.stop() == {}
