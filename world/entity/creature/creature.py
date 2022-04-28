"""
    大生物是占据位置的生物
"""

from world.entity.entity import Entity
from abc import ABCMeta, abstractmethod


class Creature(Entity, metaclass=ABCMeta):
    def __init__(self, position, life=5):
        super(Creature, self).__init__(position)
        self.life = life

    @abstractmethod
    def die(self):
        pass

    def get_life(self):
        return self.life


