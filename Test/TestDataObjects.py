from copy import deepcopy
from random import sample
from Framework.DataConstants import MIN_HIT_POINTS, MAX_HIT_POINTS
from Framework.DataObjects import PkmTemplate
from Framework.DataTypes import PkmType
from Framework.StandardPkmMoves import STANDARD_MOVE_ROSTER
import unittest
import random
import numpy as np
import itertools


class TestEncodingMethods(unittest.TestCase):

    def test_PkmMove_eq(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        for move in moves:
            move_copy = deepcopy(move)
            self.assertEqual(move, move_copy)

    def test_PkmMove_eq_name(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        for move in moves:
            move_copy = deepcopy(move)
            move_copy.name = None
            self.assertEqual(move, move_copy)

    def test_PkmMove_eq_pp(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        for move in moves:
            move_copy = deepcopy(move)
            move_copy.pp = 0
            self.assertEqual(move, move_copy)

    def test_PkmMove_ne(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        for move in moves:
            move_copy = deepcopy(move)
            move_copy.power += 1.
            self.assertNotEqual(move, move_copy)

    def test_PkmMoveRoster_eq(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        move_roster = set(moves)
        copy = deepcopy(move_roster)
        self.assertEqual(move_roster, copy)

    def test_PkmMoveRoster_eq_name(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        move_roster = set(moves)
        copy = deepcopy(move_roster)
        for move in move_roster:
            move.name = None
        self.assertEqual(move_roster, copy)

    def test_PkmMoveRoster_eq_pp(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        move_roster = set(moves)
        copy = deepcopy(move_roster)
        for move in move_roster:
            move.pp = 0
        self.assertEqual(move_roster, copy)

    def test_PkmMoveRoster_ne(self):
        moves = sample(STANDARD_MOVE_ROSTER, 10)
        move_roster = set(moves)
        move_roster_2 = set(set(moves[:-1]))
        self.assertNotEqual(move_roster, move_roster_2)
        for move in move_roster:
            move.power += 1
        move_roster_3 = set(moves)
        self.assertNotEqual(move_roster, move_roster_3)

    def test_PkmMoveRoster_in(self):
        moves = sample(STANDARD_MOVE_ROSTER, 20)
        move_roster = set(moves[:10])
        for move in moves[:10]:
            self.assertTrue(move in move_roster)
        for move in moves[10:]:
            self.assertFalse(move in move_roster)

    def test_PkmTemplate(self):
        for _ in range(10):
            pkm_type = random.choice(list(PkmType))
            max_hp = np.random.uniform(MIN_HIT_POINTS, MAX_HIT_POINTS, 1)[0]
            move_roster = set(sample(STANDARD_MOVE_ROSTER, 10))
            template = PkmTemplate(pkm_type=pkm_type, max_hp=max_hp, move_roster=move_roster)
            move_combinations = itertools.combinations(range(10), 4)
            for idx in sample(list(move_combinations), 1):
                pkm = template.gen_pkm(moves=list(idx))
                self.assertTrue(template.is_speciman(pkm))


if __name__ == '__main__':
    unittest.main()
