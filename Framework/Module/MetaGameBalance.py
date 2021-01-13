from Framework.Competition.CompetitionObjects import Competitor
from Framework.DataObjects import MetaData, PkmRoster
from Framework.Process.RosterBalance import RosterBalance


class MetaGameBalance:

    def __init__(self, c: Competitor, roster: PkmRoster):
        self.c = c
        self.roster = roster
        self.out_roster = None

    def run(self):
        rb = RosterBalance(self.c.balance_policy, self.c.meta_data, self.roster)
        self.out_roster = rb.get_roster()
