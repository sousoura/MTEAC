from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
    @abstractmethod
    def evolution(self):
        pass

    @abstractmethod
    def expansion(self):
        pass
