import unittest
from random import sample
from typing import List

from metagame_balance.vgc.competition import legal_move_set, legal_team
from metagame_balance.vgc.datatypes.Objects import PkmTemplate, Pkm, PkmFullTeam
from metagame_balance.vgc.datatypes.Types import PkmType
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomMoveRosterGenerator, RandomPkmRosterGenerator


class TestEncodingMethods(unittest.TestCase):

    def test_legal_move_set(self):
        pkm_type = PkmType.NORMAL
        move_roster_generator = RandomMoveRosterGenerator(pkm_type=pkm_type)
        move_roster = move_roster_generator.gen_roster()
        template = PkmTemplate(move_roster, pkm_type, 180., 0)
        for _ in range(10):
            moves: List[int] = sample(range(move_roster_generator.n_moves_pkm), 4)
            pkm = template.gen_pkm(moves)
            self.assertTrue(legal_move_set(pkm, template))
        move_roster_2 = move_roster_generator.gen_roster()
        template_2 = PkmTemplate(move_roster_2, pkm_type, 180., 1)
        for _ in range(10):
            moves: List[int] = sample(range(move_roster_generator.n_moves_pkm), 4)
            pkm = template.gen_pkm(moves)
            self.assertFalse(legal_move_set(pkm, template_2))

    def test_legal_team(self):
        pkm_roster_generator = RandomPkmRosterGenerator()
        roster = pkm_roster_generator.gen_roster()
        for _ in range(10):
            pkms: List[Pkm] = [template.gen_pkm(sample(range(pkm_roster_generator.n_moves_pkm), 6)) for template in
                               sample(roster, 6)]
            team = PkmFullTeam(pkms)
            self.assertTrue(legal_team(team, roster))
        roster_2 = pkm_roster_generator.gen_roster()
        for _ in range(10):
            pkms: List[Pkm] = [template.gen_pkm(sample(range(pkm_roster_generator.n_moves_pkm), 6)) for template in
                               sample(roster, 6)]
            team = PkmFullTeam(pkms)
            self.assertFalse(legal_team(team, roster_2))


if __name__ == '__main__':
    unittest.main()
