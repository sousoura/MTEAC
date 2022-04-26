"""
    大动物是占据位置而且能运动的大生物
"""

from world.entity.big_entity.big_creature.big_creature import Big_creature
from world.entity.active_thing import Active_thing
from abc import ABCMeta, abstractmethod


class Big_animal(Big_creature, Active_thing, metaclass=ABCMeta):
    def __init__(self, position, life=5):
        super(Big_animal, self).__init__(position, life)

    @abstractmethod
    def move(self, new_position):
        pass

    @abstractmethod
    def get_perception(self, terrain, things_position):
        pass
