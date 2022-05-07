from world.entity.entity_import import *
from abc import ABCMeta, abstractmethod


class Plant(Creature, Food, metaclass=ABCMeta):
    def __init__(self, position, leaf_content=50, carapace=10):
        Creature.__init__(self, position, carapace=10)
        Food.__init__(self, leaf_content)

    @abstractmethod
    def die(self):
        pass
