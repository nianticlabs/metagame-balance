import unittest

from framework.balance.archtype import standard_move_distance
from framework.util.generator.StandardPkmMoves import SunnyDay, FireBlast, Flamethrower, HydroPump, STANDARD_MOVE_ROSTER


class TestDistance(unittest.TestCase):

    def test_set_move_similarity_1(self):
        for move in STANDARD_MOVE_ROSTER:
            self.assertEqual(standard_move_distance(move, move), 0.0)

    def test_set_move_similarity_2(self):
        for move0, move1 in zip(STANDARD_MOVE_ROSTER, STANDARD_MOVE_ROSTER):
            self.assertEqual(standard_move_distance(move0, move1), standard_move_distance(move1, move0))

    def test_set_move_similarity_3(self):
        self.assertGreater(standard_move_distance(SunnyDay, FireBlast), standard_move_distance(Flamethrower, FireBlast))
        self.assertGreater(standard_move_distance(HydroPump, FireBlast),
                           standard_move_distance(Flamethrower, FireBlast))
        self.assertGreater(standard_move_distance(HydroPump, FireBlast), standard_move_distance(Flamethrower, SunnyDay))
