import itertools
import random
import unittest
from copy import deepcopy

from metagame_balance.vgc.competition.StandardPkmMoves import STANDARD_MOVE_ROSTER
from metagame_balance.vgc.datatypes.Constants import BASE_HIT_POINTS, MAX_HIT_POINTS
from metagame_balance.vgc.datatypes.Objects import PkmTemplate, PkmTeam, GameState, Weather
from metagame_balance.vgc.datatypes.Types import PkmType
from metagame_balance.vgc.util.Encoding import decode_move, encode_move, encode_pkm, decode_pkm, encode_team, decode_team, \
    encode_game_state, decode_game_state


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
            max_hp = random.randint(BASE_HIT_POINTS, MAX_HIT_POINTS)
            move_roster = set(random.sample(deepcopy(STANDARD_MOVE_ROSTER), 10))
            template = PkmTemplate(pkm_type=pkm_type, max_hp=max_hp, move_roster=move_roster)
            move_combinations = itertools.combinations(range(10), 4)
            for idx in random.sample(list(move_combinations), 1):
                pkm = template.gen_pkm(moves=list(idx))
                e = []
                encode_pkm(e, pkm)
                d = decode_pkm(e)
                self.assertEqual(pkm, d)

    def test_encode_team(self):
        for _ in range(10):
            pkm_type = random.choice(list(PkmType))
            max_hp = random.randint(BASE_HIT_POINTS, MAX_HIT_POINTS)
            move_roster = set(random.sample(deepcopy(STANDARD_MOVE_ROSTER), 10))
            template = PkmTemplate(pkm_type=pkm_type, max_hp=max_hp, move_roster=move_roster)
            move_combinations = itertools.combinations(range(10), 4)
            pkms = []
            for idx in random.sample(list(move_combinations), 3):
                pkms.append(template.gen_pkm(moves=list(idx)))
            team = PkmTeam(pkms)
            e = []
            encode_team(e, team)
            d = decode_team(e)
            self.assertEqual(team, d)

    def test_encode_game_state(self):
        for _ in range(10):
            pkm_type = random.choice(list(PkmType))
            max_hp = random.randint(BASE_HIT_POINTS, MAX_HIT_POINTS)
            move_roster = set(random.sample(deepcopy(STANDARD_MOVE_ROSTER), 10))
            template = PkmTemplate(pkm_type=pkm_type, max_hp=max_hp, move_roster=move_roster)
            move_combinations = itertools.combinations(range(10), 4)
            pkms = []
            for idx in random.sample(list(move_combinations), 3):
                pkms.append(template.gen_pkm(moves=list(idx)))
            team = PkmTeam(pkms)
            game_state = GameState([team, team], Weather())
            e = []
            encode_game_state(e, game_state)
            d = decode_game_state(e)
            self.assertEqual(game_state, d)


if __name__ == '__main__':
    unittest.main()
