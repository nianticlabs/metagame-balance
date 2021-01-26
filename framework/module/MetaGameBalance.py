from framework.competition.CompetitionObjects import Competitor
from framework.DataObjects import MetaData, PkmRoster
from framework.process.RosterBalance import RosterBalance


class MetaGameBalance:

    def __init__(self, c: Competitor, roster: PkmRoster):
        self.c = c
        self.roster = roster
        self.out_roster = None

    def run(self):
        rb = RosterBalance(self.c.balance_policy, self.c.meta_data, self.roster)
        self.out_roster = rb.get_roster()
