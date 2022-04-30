"""
    大动物是占据位置而且能运动的大生物
"""

from world.entity.creature.creature import Creature
from world.entity.active_thing import Active_thing
from abc import ABCMeta, abstractmethod


class Animal(Creature, Active_thing, metaclass=ABCMeta):

    def __init__(self, position, life, brain):
        super(Animal, self).__init__(position, life)
        self.brain = brain

    @abstractmethod
    def move(self, new_position):
        pass

    @abstractmethod
    def get_perception(self, terrain, things_position):
        pass

    # 想出一个行为
    def devise_an_act(self, perception):
        return self.brain.devise_an_act(perception, self)
