from abc import ABCMeta, abstractmethod


class World_generator(metaclass=ABCMeta):
    @abstractmethod
    def generate(self, world, state):
        pass
