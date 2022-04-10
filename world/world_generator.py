from abc import ABCMeta, abstractmethod


class World_generator(metaclass=ABCMeta):
    @abstractmethod
    def generate_a_world(self):
        pass
