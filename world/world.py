from abc import ABCMeta, abstractmethod


class World(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def evolution_a_turn(self):
        pass

    @abstractmethod
    def expansion(self):
        pass

    @abstractmethod
    def evolution(self):
        pass
