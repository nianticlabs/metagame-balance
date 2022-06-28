

class MC_Agent():
    """
    Responsible for maintaining the utility function
    Specially:
    1) Update the utility function
    2) return/retain two versions for two agents
    3) Perhaps keep pointer to them
    """
    def __init__(self):

        self.U # Neural network!!

    def update(self, team, reward) -> None:

        raise NotImplementedError

    def get_agent_U_function(self):

        raise NotImplementedError

    def get_adversary_U_function(self):

        raise NotImplementedError
