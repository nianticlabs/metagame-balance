import unittest

from vgc.balance.archtype import std_move_dist
from vgc.competition.StandardPkmMoves import SunnyDay, FireBlast, Flamethrower, HydroPump, STANDARD_MOVE_ROSTER


class TestDistance(unittest.TestCase):

    def test_set_move_similarity_1(self):
        for move in STANDARD_MOVE_ROSTER:
            self.assertEqual(std_move_dist(move, move), 0.0)

    def test_set_move_similarity_2(self):
        for move0, move1 in zip(STANDARD_MOVE_ROSTER, STANDARD_MOVE_ROSTER):
            self.assertEqual(std_move_dist(move0, move1), std_move_dist(move1, move0))

    def test_set_move_similarity_3(self):
        self.assertGreater(std_move_dist(SunnyDay, FireBlast), std_move_dist(Flamethrower, FireBlast))
        self.assertGreater(std_move_dist(HydroPump, FireBlast),
                           std_move_dist(Flamethrower, FireBlast))
        self.assertGreater(std_move_dist(HydroPump, FireBlast), std_move_dist(Flamethrower, SunnyDay))
