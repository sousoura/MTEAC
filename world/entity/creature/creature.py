"""
    生物是有生命 会死亡的物体
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

    def is_die(self):
        return self.life <= 0

    def get_life(self):
        return self.life


