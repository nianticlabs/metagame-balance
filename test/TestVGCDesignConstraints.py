import unittest

from metagame_balance.vgc.balance.restriction import VGCDesignConstraints, RosterBoundedSizeRule, RosterFixedSizeRule, \
    UnbannableRule, MoveRosterBoundedSizeRule, MoveRosterFixedSizeRule, MovesUnchangeableRule, TypeUnchangeableRule, \
    MaxHPUnchangeableRule
from metagame_balance.vgc.datatypes.Types import PkmType
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


class TestVGCDesignConstraints(unittest.TestCase):

    def test_check_every_rule(self):
        gen = RandomPkmRosterGenerator()
        roster = gen.gen_roster()
        constraints = VGCDesignConstraints(roster)
        constraints.add_global_rule(RosterBoundedSizeRule(roster, max_size=len(roster)))
        constraints.add_global_rule(RosterFixedSizeRule(roster))
        constraints.add_global_rule(UnbannableRule(roster, list(roster)[0]))
        constraints.add_pkm_rule(list(roster)[1], MoveRosterBoundedSizeRule(roster))
        constraints.add_pkm_rule(list(roster)[2], MoveRosterFixedSizeRule(roster, list(roster)[2].move_roster))
        constraints.add_pkm_rule(list(roster)[3], MovesUnchangeableRule(roster, list(roster)[3].move_roster))
        constraints.add_pkm_rule(list(roster)[4], TypeUnchangeableRule(roster, list(roster)[4].type))
        constraints.add_pkm_rule(list(roster)[5], MaxHPUnchangeableRule(roster, list(roster)[5].max_hp))
        failed = constraints.check_every_rule(roster)
        self.assertEqual(len(failed), 0)
        list(roster)[5].max_hp -= 1.0
        failed = constraints.check_every_rule(roster)
        self.assertEqual(len(failed), 1)
        list(roster)[4].type = PkmType.NORMAL if list(roster)[4].type != PkmType.NORMAL else PkmType.FIRE
        failed = constraints.check_every_rule(roster)
        self.assertEqual(len(failed), 2)
        list(roster)[3].move_roster.pop()
        failed = constraints.check_every_rule(roster)
        self.assertEqual(len(failed), 3)
        list(roster)[2].move_roster.pop()
        failed = constraints.check_every_rule(roster)
        self.assertEqual(len(failed), 4)
        roster.pop()
        failed = constraints.check_every_rule(roster)
        self.assertEqual(len(failed), 6)
