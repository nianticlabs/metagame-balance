import itertools
import random
import unittest
from copy import deepcopy
from decimal import Decimal

import numpy as np

from Framework.DataConstants import MIN_HIT_POINTS, MAX_HIT_POINTS
from Framework.DataObjects import PkmTemplate
from Framework.DataTypes import PkmType
from Framework.StandardPkmMoves import STANDARD_MOVE_ROSTER
from Util.Encoding import decode_move, encode_move, encode_pkm, decode_pkm


class TestEncodingMethods(unittest.TestCase):

    def test_encode_move(self):
        for move in STANDARD_MOVE_ROSTER:
            e = []
            encode_move(e, move)
            d = decode_move(e)
            self.assertEqual(move, d)

    def test_encode_pkm(self):
        for _ in range(100):
            pkm_type = random.choice(list(PkmType))
            max_hp = random.randint(MIN_HIT_POINTS, MAX_HIT_POINTS)
            move_roster = set(random.sample(deepcopy(STANDARD_MOVE_ROSTER), 10))
            template = PkmTemplate(pkm_type=pkm_type, max_hp=max_hp, move_roster=move_roster)
            move_combinations = itertools.combinations(range(10), 4)
            for idx in random.sample(list(move_combinations), 1):
                pkm = template.gen_pkm(moves=list(idx))
                e = []
                encode_pkm(e, pkm)
                d = decode_pkm(e)
                self.assertEqual(pkm, d)


if __name__ == '__main__':
    unittest.main()
