import numpy as np

class RPSFWTeam():
    def __init__(self):

        self.item = -1 ##item not selected!

    def mark(self, item: int):
        assert(self.item == -1)
        assert(item >= 0 and item <= 4)
        self.item = item

    def __getitem__(self,idx: int):
        if idx == 0 or idx == -1:
            return self.item

        raise Exception("Only one idx available for RPSFW")


    def __len__(self):
        return 1

def predict(u):
    """
    U is the policy for RPSFW
    """
    vals = u.get_all_vals()

    def batch_predictor(teams):
        u = np.zeros((len(teams)))

        for i, team in enumerate(teams):
            u[i] = vals[team[0]] # coz rpsfw has one item
        return vals

    return batch_predictor


