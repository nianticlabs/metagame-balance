import numpy as np


class TabularFn:
    """"""
    def __init__(self, size: int):
        self.V = np.zeros(size)

    def get_all_vals(self):
        return self.V

    def __getitem__(self, item):

        return self.V[item]

    def __setitem__(self, key, value):

        self.V[key] = value
