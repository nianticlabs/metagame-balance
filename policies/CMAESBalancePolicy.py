from vgc.behaviour import BalancePolicy
from vgc.balance import DeltaRoster, DeltaPkm
from vgc.balance.meta import MetaData
from vgc.balance.restriction import DesignConstraints
from vgc.behaviour import BalancePolicy
from vgc.datatypes.Objects import PkmRoster
from vgc.util.RosterParsers import MetaRosterStateParser
from typing import Tuple
import copy

class CMAESBalancePolicy(BalancePolicy):

    def __init__(self, num_pkm):
        
        self.parser = MetaRosterStateParser(num_pkm)
        self.num_pkm = num_pkm 
        self.state = None

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> DeltaRoster:
       
        meta_data = d[1]
        state = self.parser.metadata_to_state(meta_data)
    
        #print(state, len(state))
        if self.state is not None:
            assert(state == self.state)
        return self.parser.state_to_delta_roster(state, meta_data)
        #return DeltaRoster({pkm.pkm_id: DeltaPkm(2., pkm.type, delta_pkm)})
