"""
    生物是有生命 会死亡的物体
"""

from world.entity.entity import Entity
from abc import ABCMeta, abstractmethod


class Creature(Entity, metaclass=ABCMeta):
    def __init__(self, position, life=100, carapace=0):
        super(Creature, self).__init__(position)
        self.life = life
        self.carapace = carapace

    # @abstractmethod
    # def die(self):
    #     pass

    def get_life(self):
        return self.life

    def be_attack(self, aggressivity):
        self.life -= max(aggressivity - self.carapace, 0) / (self.carapace + 1)

    def is_die(self):
        return self.life <= 0

    @abstractmethod
    def die(self):
        pass
