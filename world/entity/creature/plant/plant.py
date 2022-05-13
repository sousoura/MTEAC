from world.entity.obj.food import Food
from world.entity.creature.creature import Creature
from abc import ABCMeta, abstractmethod


class Plant(Creature, Food, metaclass=ABCMeta):
    def __init__(self, position, leaf_content=50, carapace=10):
        Creature.__init__(self, position, carapace=carapace)
        Food.__init__(self, leaf_content)

    @abstractmethod
    def die(self):
        pass

    def post_turn_change(self):
        pass
