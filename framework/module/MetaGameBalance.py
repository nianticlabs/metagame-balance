from framework.competition.CompetitionObjects import Competitor
from framework.DataObjects import PkmRoster, DesignConstraints
from framework.process.RosterBalance import RosterBalance


class MetaGameBalance:

    def __init__(self, c: Competitor, roster: PkmRoster, constraints: DesignConstraints):
        self.c = c
        self.rb = RosterBalance(self.c.balance_policy, self.c.meta_data, roster, constraints)

    def run(self):
        self.rb.run()

    def output(self) -> PkmRoster:
        return self.rb.roster
