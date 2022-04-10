from abc import ABCMeta, abstractmethod


class world(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state):
        pass

    @abstractmethod
    def evolution(self):
        pass

    @abstractmethod
    def expansion(self):
        pass
