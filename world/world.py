from abc import ABCMeta, abstractmethod


# 抽象的世界类
class World(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def expansion(self):
        pass

    @abstractmethod
    def evolution(self):
        pass
