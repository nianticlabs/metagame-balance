from vgc.behaviour import BalancePolicy
from vgc.balance import DeltaRoster, DeltaPkm
from vgc.balance.meta import MetaData
from vgc.balance.restriction import DesignConstraints
from vgc.behaviour import BalancePolicy
from vgc.datatypes.Objects import PkmRoster
from typing import Tuple
import copy
class CMAESBalancePolicy(BalancePolicy):

    def __init__(self):
        
        pass
        #self.model 

    def close(self):
        pass

    def get_action(self, d: Tuple[PkmRoster, MetaData, DesignConstraints]) -> DeltaRoster:
      
        pkm = list(d[0])[0]
        delta_pkm = {}
        for i, move in enumerate(pkm.move_roster):
            print(move, move.power)
            move.power += 12
            delta_pkm[i] = move
        #pkm = d[0].get_pkm_template_view(0)
        #moves = [pkm.get_move_roster_view().get_move_view(i) for i in range(4)]
        #print(pkm, moves)
        #return DeltaRoster({0: DeltaPkm(2, 3, {pkm.move_roster})})
        return DeltaRoster({pkm.pkm_id: DeltaPkm(2., pkm.type, delta_pkm)})
