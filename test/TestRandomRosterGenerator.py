import unittest

from metagame_balance.vgc.competition import get_pkm_points, STANDARD_TOTAL_POINTS
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


class TestEncodingMethods(unittest.TestCase):

    def test_random_roster_generator(self):
        gen = RandomPkmRosterGenerator()
        roster = gen.gen_roster()
        for tmpl in roster:
            pkm = tmpl.gen_pkm([0, 1, 2, 3])
            print(pkm)
            points = get_pkm_points(pkm)
            print(points)
            self.assertLess(points, STANDARD_TOTAL_POINTS + 1)
