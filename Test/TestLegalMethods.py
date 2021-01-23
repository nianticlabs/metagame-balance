import unittest

from Framework.Competition import legal_move_set
from Util.PkmRosterGenerators import StandardPkmRosterGenerator


class TestEncodingMethods(unittest.TestCase):

    def test_legal_move_set(self):
        roster_generator = StandardPkmRosterGenerator()
        legal_move_set()


if __name__ == '__main__':
    unittest.main()
