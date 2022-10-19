import logging
import operator

from metagame_balance.agent.Example_Competitor import ExampleCompetitor
from metagame_balance.agent.Fixed_Team_Competitor import FixedTeamCompetitor
from metagame_balance.vgc.balance.meta import MetaData
from metagame_balance.vgc.competition import CompetitorManager, legal_team
from metagame_balance.vgc.competition.random_competitor import RandomTeamSelectionCompetitor
from metagame_balance.vgc.datatypes.Constants import DEFAULT_MATCH_N_BATTLES, DEFAULT_TEAM_SIZE
from metagame_balance.vgc.datatypes.Objects import PkmRoster, get_pkm_roster_view
from metagame_balance.vgc.ecosystem.BattleEcosystem import BattleEcosystem, Strategy
from metagame_balance.vgc.util.generator.PkmTeamGenerators import RandomTeamFromRoster

from tqdm.auto import tqdm

class ChampionshipEcosystem:

    def __init__(self, roster: PkmRoster, meta_data: MetaData, debug=False, render=False,
                 n_battles=DEFAULT_MATCH_N_BATTLES, strategy: Strategy = Strategy.RANDOM_PAIRING,
                 team_size: int = DEFAULT_TEAM_SIZE):
        self.meta_data = meta_data
        self.roster = roster
        self.roster_view = get_pkm_roster_view(self.roster)
        self.rand_gen = RandomTeamFromRoster(self.roster)
        self.league: BattleEcosystem = BattleEcosystem(self.meta_data, debug, render, n_battles, strategy,
                                                       update_meta=True, full_team_size=team_size)
        self.debug = debug
        self.team_size = team_size

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
        for epoch in tqdm(range(n_epochs), desc="stage2_iter"):
            self.simulate_league(n_league_epochs)

            for cm in self.league.competitors:
                reward = self.get_reward(cm)
                cm.competitor.team_build_policy.update(cm.team, reward)  # TODO: Define a reward function

            self.league.clear_wins()  # do we really need this?
            if epoch % 100 == 0:
                # after every 100 matches check how good are we against random bot
                logging.info("Testing agent vs random")
                self.test_agent(n_league_epochs)

        # info for debugging and resetting test rewards
        logging.info("test_rewards: %s, avg reward : %f", str(self.test_rewards),
                     sum(self.test_rewards) / len(self.test_rewards))
        self.test_rewards = []

    def get_reward(self, cm: CompetitorManager):
        if cm.competitor.name == "adversary":
            return -self.league.get_team_wins(cm)
        elif cm.competitor.name == "agent":
            return self.league.get_team_wins(cm)
        else:
            raise Exception("Unkown Player Name")

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
        random_agent = CompetitorManager(RandomTeamSelectionCompetitor(self.team_size))

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

    def simulate_n_battles(self, n_league_epochs: int, t1, t2):
        """
        TODO: Check for instabilities introduced by this!
        """
        NUM_SIM = 10
        t1_agent = CompetitorManager(FixedTeamCompetitor("t1", t1))
        t2_agent = CompetitorManager(FixedTeamCompetitor("t2", t2))

        old_agents = []

        num_competitors = len(self.league.competitors)
        for cm in range(num_competitors):
            cm = self.league.competitors[0]
            old_agents.append(cm)
            self.league.unregister(cm)
        self.register(t1_agent)
        self.register(t2_agent)
        win_probs = 0
        for i in range(NUM_SIM):
            self.simulate_league(n_league_epochs)
        wins = self.league.get_team_wins(t1_agent)
        self.league.clear_wins()  # do we really need this?
        self.league.unregister(t1_agent)
        self.league.unregister(t2_agent)
        for cm in old_agents:
            self.league.register(cm)
        losses = (NUM_SIM) - wins
        #print(wins, losses, (wins - losses) / NUM_SIM)
        return (wins - losses)  / NUM_SIM
