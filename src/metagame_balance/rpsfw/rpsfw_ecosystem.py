

class RPSFWEcosystem():

    def __init__(self, metadata):

        self.players = []
        self.metadata = metadata
        self.battle_env = RPSFWBattle()

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
            selt.battle_env.batttle()


