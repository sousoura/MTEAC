"""
    人类是能使用技能 工具 会学习 有背包且有社会性的动物
"""

from world.entity.creature.animal.animal import Animal
from abc import ABCMeta, abstractmethod


class Human(Animal, metaclass=ABCMeta):
    pass

