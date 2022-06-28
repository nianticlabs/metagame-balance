from vgc.behaviour import TeamSelectionPolicy
from vgc.competition.Competitor import Competitor
from agent.MC_Agent import MC_Agent #change name!!

class SeqSoftmaxCompetitor(Competitor):

    def __init__(self, name: str):
        self._name = name
        self._team_selection_policy = #create a policy based on U!

    @property
    def name(self):
        return self._name

    @property
    def team_selection_policy(self) -> TeamSelectionPolicy:
        return self._team_selection_policy
