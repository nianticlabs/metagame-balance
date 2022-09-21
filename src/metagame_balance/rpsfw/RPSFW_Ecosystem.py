import typing

from metagame_balance.rpsfw.Rosters import RPSFWRoster
from metagame_balance.rpsfw.SoftmaxCompetitor import SoftmaxCompetitor
from metagame_balance.rpsfw.battle import RPSFWBattle
from metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData

from tqdm import tqdm


class RPSFWEcosystem:

    def __init__(self, metadata: PolicyEntropyMetaData):
        self.players: typing.List[SoftmaxCompetitor] = []
        self.metadata = metadata
        self.roster = RPSFWRoster(metadata)
        self.battle_env = RPSFWBattle(metadata)

    def register(self, player):
        if len(self.players) >= 2:
            raise Exception("Number of players in rock.. cannot be greater than 2")
        self.players.append(player)

    def unregister(self, player):
        if len(self.players) == 0:
            raise Exception("Number of players in rock.. cannot be less than 0")
        self.players.remove(player)

    def run(self, epochs):
        for _ in tqdm(range(epochs)):
            item1, item2 = self.players[0].get_action(self.roster), \
                           self.players[1].get_action(self.roster)
            items = [item1, item2]
            reward = self.battle_env.battle(item1, item2)
            for i, player in enumerate(self.players):
                player.update(items[i], reward)

    def test_agent(self):
        pass #NotImplementedError
