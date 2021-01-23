import unittest
from random import sample
from typing import List
from Framework.Competition import legal_move_set, legal_team
from Framework.DataObjects import PkmTemplate, PkmTeam, Pkm
from Framework.DataTypes import PkmType
from Util.PkmRosterGenerators import RandomMoveRosterGenerator, RandomPkmRosterGenerator


class TestEncodingMethods(unittest.TestCase):

    def test_legal_move_set(self):
        pkm_type = PkmType.NORMAL
        move_roster_generator = RandomMoveRosterGenerator(pkm_type=pkm_type)
        move_roster = move_roster_generator.gen_roster()
        template = PkmTemplate(move_roster=move_roster, pkm_type=pkm_type, max_hp=180.)
        for _ in range(10):
            moves: List[int] = sample(range(move_roster_generator.n_moves_pkm), 4)
            pkm = template.gen_pkm(moves)
            self.assertTrue(legal_move_set(pkm, template))
        move_roster_2 = move_roster_generator.gen_roster()
        template_2 = PkmTemplate(move_roster=move_roster_2, pkm_type=pkm_type, max_hp=180.)
        for _ in range(10):
            moves: List[int] = sample(range(move_roster_generator.n_moves_pkm), 4)
            pkm = template.gen_pkm(moves)
            self.assertFalse(legal_move_set(pkm, template_2))

    def test_legal_team(self):
        pkm_roster_generator = RandomPkmRosterGenerator()
        roster = pkm_roster_generator.gen_roster()
        for _ in range(10):
            pkms: List[Pkm] = [template.gen_pkm(sample(range(pkm_roster_generator.n_moves_pkm), 4)) for template in
                               sample(roster, 6)]
            team = PkmTeam(pkms)
            self.assertTrue(legal_team(team, roster))
        roster_2 = pkm_roster_generator.gen_roster()
        for _ in range(10):
            pkms: List[Pkm] = [template.gen_pkm(sample(range(pkm_roster_generator.n_moves_pkm), 4)) for template in
                               sample(roster, 6)]
            team = PkmTeam(pkms)
            self.assertFalse(legal_team(team, roster_2))


if __name__ == '__main__':
    unittest.main()
