"""
    大生物是占据位置的生物
"""

from world.entity.big_entity.big_entity import Big_entity
from abc import ABCMeta, abstractmethod


class Big_creature(Big_entity, metaclass=ABCMeta):
    def __init__(self, position, life=5):
        super(Big_creature, self).__init__(position)
        self.life = life
