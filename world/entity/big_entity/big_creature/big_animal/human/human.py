"""
    人类是能使用技能的大动物
"""

from world.entity.big_entity.big_creature.big_animal.big_animal import Big_animal
from abc import ABCMeta, abstractmethod


class Human(Big_animal):
    def __init__(cls, position, life):
        super(Human, cls).__init__(position, life)

    @abstractmethod
    def move(self, new_position):
        pass
