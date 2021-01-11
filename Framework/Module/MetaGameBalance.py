from Framework.Competition.CompetitionStructures import Competitor
from Framework.DataObjects import MetaData, PkmRoster
from Framework.Process.RosterBalance import RosterBalance


class MetaGameBalance:

    def __init__(self, c: Competitor, meta_data: MetaData, roster: PkmRoster):
        self.c = c
        self.meta_data = meta_data
        self.roster = roster
        self.out_roster = None

    def run(self):
        rb = RosterBalance(self.c.balance_policy, self.meta_data, self.roster)
        self.out_roster = rb.get_roster()
