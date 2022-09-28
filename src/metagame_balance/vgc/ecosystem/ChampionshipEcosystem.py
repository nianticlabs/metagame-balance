import logging
import operator

from tqdm import tqdm
from metagame_balance.agent.Example_Competitor import ExampleCompetitor
from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.competition import CompetitorManager, legal_team
from metagame_balance.vgc.datatypes.Constants import DEFAULT_MATCH_N_BATTLES
from metagame_balance.vgc.datatypes.Objects import PkmRoster, get_pkm_roster_view
from metagame_balance.vgc.ecosystem.BattleEcosystem import BattleEcosystem, Strategy
from metagame_balance.vgc.util.generator.PkmTeamGenerators import RandomTeamFromRoster


class ChampionshipEcosystem:

    def __init__(self, roster: PkmRoster, meta_data: MetaData, debug=False, render=False,
                 n_battles=DEFAULT_MATCH_N_BATTLES, strategy: Strategy = Strategy.RANDOM_PAIRING):
        self.meta_data = meta_data
        self.roster = roster
        self.roster_view = get_pkm_roster_view(self.roster)
        self.rand_gen = RandomTeamFromRoster(self.roster)
        self.league: BattleEcosystem = BattleEcosystem(self.meta_data, debug, render, n_battles, strategy,
                                                       update_meta=True)
        self.debug = debug

        self.test_rewards = []

    def register(self, cm: CompetitorManager):
        self.league.register(cm)

    def simulate_league(self, n_league_epochs: int):
        if self.debug:
            print("TEAM BUILD\n")
        for cm in self.league.competitors:
            self.__set_new_team(cm)
            if self.debug:
                print(cm.competitor.name)
                print(cm.team)
                print()
        if self.debug:
            print("LEAGUE\n")
        self.league.run(n_league_epochs)

    def run(self, n_epochs: int, n_league_epochs: int):
        """
        For every epoch in n_epochs, simulate the whole league for n_league_epochs.
        """
        for epoch in range(n_epochs):
            self.simulate_league(n_league_epochs)

            for cm in self.league.competitors:
                reward = self.get_reward(cm)
                cm.competitor.team_build_policy.update(cm.team, reward)  # TODO: Define a reward function

            self.league.clear_wins()  # do we really need this?
            if epoch % 100 == 0:
                # after every 100 matches check how good are we against random bot
                self.test_agent(n_league_epochs)

        # info for debugging and resetting test rewards
        logging.info("test_rewards: %s, avg reward : %f", str(self.test_rewards),
                     sum(self.test_rewards) / len(self.test_rewards))
        self.test_rewards = []

    def get_reward(self, cm: CompetitorManager):
        return self.league.get_team_wins(cm)

    def __set_new_team(self, cm: CompetitorManager):

        """
        No try except (masks the error). I do not see any reason why it should fail
        """
        cm.team = cm.competitor.team_build_policy.get_action((self.meta_data, cm.team, self.roster))
        if not legal_team(cm.team, self.roster):
            print("Not legal team")
            cm.team = self.rand_gen.get_team()

    def strongest(self) -> CompetitorManager:
        return max(self.league.competitors, key=operator.attrgetter('elo'))

    def test_agent(self, n_league_epochs: int):
        """
        TODO: Check for instabilities introduced by this!
        """
        random_agent = CompetitorManager(ExampleCompetitor())

        learnt_cm = None
        adversary_cm = None
        for cm in self.league.competitors:
            if cm.competitor.name == "adversary":
                adversary_cm = cm
            if cm.competitor.name == "agent":
                learnt_cm = cm
        self.league.unregister(adversary_cm)
        self.register(random_agent)
        rewards = 0
        learnt_cm.competitor.team_build_policy.set_greedy(greedy=True)
        for i in range(100):
            self.simulate_league(n_league_epochs)
            # print(self.get_reward(learnt_cm), self.get_reward(random_agent))
        self.test_rewards.append(self.get_reward(learnt_cm))
        self.league.clear_wins()  # do we really need this?
        self.register(adversary_cm)
        self.league.unregister(random_agent)
        learnt_cm.competitor.team_build_policy.set_greedy(greedy=False)
