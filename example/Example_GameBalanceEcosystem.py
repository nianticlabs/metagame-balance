from typing import List

from example.Example_Competitor import ExampleCompetitor
from vgc.balance.meta import MetaData
from vgc.balance.restriction import DesignConstraints, DesignRule
from vgc.datatypes.Objects import PkmRosterView, PkmRoster, PkmTemplate
from vgc.ecosystem.GameBalanceEcosystem import GameBalanceEcosystem
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

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

    def check_every_rule(self, roster: PkmRoster) -> List[DesignRule]:
        pass

    def __init__(self, base_roster):
        self.base_roster = base_roster

    def base_roster(self) -> PkmRosterView:
        pass


def main():
    roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
    mdc = MockDesignConstraints(roster)
    meta_data = MetaData()
    be = GameBalanceEcosystem(ExampleCompetitor(), ExampleCompetitor(), mdc, roster, meta_data, debug=True, render=True,
                              n_competitors=N_PLAYERS)
    be.run(n_vgc_epochs=10, n_league_epochs=10)


if __name__ == '__main__':
    main()
