from abc import ABCMeta, abstractmethod


class World_generator:
    @abstractmethod
    def generate(self, world, state):
        pass
