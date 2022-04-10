from abc import ABCMeta, abstractmethod
from state import State


class World(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def evolution(self):
        pass

    @abstractmethod
    def expansion(self):
        pass
