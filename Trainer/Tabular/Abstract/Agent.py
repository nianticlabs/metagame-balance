from abc import ABC, abstractmethod


class Agent(ABC):

    @abstractmethod
    def check_state(self, s):
        pass

    @abstractmethod
    def get_action(self, s):
        pass

    @abstractmethod
    def update(self, s0, s1, a, r, t):
        pass
