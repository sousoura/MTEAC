"""
    人类是能使用技能的大动物
"""

from world.entity.creature.animal.animal import Animal
from abc import ABCMeta, abstractmethod


class Human(Animal):
    def __init__(cls, position, life):
        super(Human, cls).__init__(position, life)

    @abstractmethod
    def move(self, new_position):
        pass
