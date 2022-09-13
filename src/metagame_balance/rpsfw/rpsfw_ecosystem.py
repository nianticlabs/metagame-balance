from metagame_balance.rpsfw.battle import RPSFWBattle
from metagame_balance.rpsfw.balance.Policy_Entropy_Meta import PolicyEntropyMetaData 

class RPSFWEcosystem():

    def __init__(self, metadata: PolicyEntropyMetaData):

        self.players = []
        self.metadata = metadata
        self.battle_env = RPSFWBattle(metadata)

    def register(self, player):

        if len(self.players) >= 2:
            raise Exception("Number of players in rock.. cannot be greater than 2")
        self.players.append(player)

    def unregister(self, player):

        if len(self.players) == 0 :
            raise Exception("Number of players in rock.. cannot be less than 0")
        self.players.remove(player)

    def run(self, epochs):

        for _ in epochs:
            item1, item2 = self.players[0].select(), self.players[1].select()
            self.battle_env.battle(item1, item2)
