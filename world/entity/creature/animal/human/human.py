"""
    人类是能使用技能 工具 会学习 有背包且有社会性的动物
"""

from world.entity.creature.animal.animal import Animal
from abc import ABCMeta, abstractmethod


class Human(Animal):
    def __init__(self, position, life, brain, health_point, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Human, self).__init__(position, life, brain, health_point, full_value, drinking_value, body_state, gender,
                                    crawl_ability, speed, aggressivity)

    @abstractmethod
    def die(self):
        pass
