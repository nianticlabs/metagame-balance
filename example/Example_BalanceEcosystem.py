from typing import List

from competitor.ExampleCompetitor import ExampleCompetitor
from framework.balance.restriction import DesignConstraints, DesignRule, Target
from framework.datatypes.Objects import PkmRosterView, PkmRoster, PkmTemplate
from framework.ecosystem.BalanceEcosystem import BalanceEcosystem
from framework.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from framework.util.Recording import DataDistributionManager

N_PLAYERS = 16


class MockDesignConstraints(DesignConstraints):

    def get_base_roster(self) -> PkmRosterView:
        pass

    def get_allpkm_rule_set(self) -> List[DesignRule]:
        pass

    def get_pkm_rule_set(self, template: PkmTemplate) -> List[DesignRule]:
        pass

    def get_global_rule_set(self) -> List[DesignRule]:
        pass

    def get_target_set(self) -> List[Target]:
        pass

    def check_every_rule(self, roster: PkmRoster) -> List[DesignRule]:
        pass

    def __init__(self, base_roster):
        self.base_roster = base_roster

    def base_roster(self) -> PkmRosterView:
        pass


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    mdc = MockDesignConstraints(roster)
    ddm = DataDistributionManager()
    be = BalanceEcosystem(ExampleCompetitor(), ExampleCompetitor(), mdc, roster, debug=True, render=True, ddm=ddm,
                          n_competitors=N_PLAYERS)
    be.run(n_vgc_epochs=10, n_league_epochs=10)


if __name__ == '__main__':
    main()
