"""
    动物是会运动 会行动的生物
"""
import random

from world.entity.creature.creature import Creature
from world.entity.active_thing import Active_thing
from abc import ABCMeta, abstractmethod


class Animal(Creature, Active_thing, metaclass=ABCMeta):

    """
        行为合法性判断
    """
    action_list = []

    @abstractmethod
    def __init__(self, position, *attrs):
        super().__init__(position)

    # 判断行动合法性 属性对行动的影响体现在此
    # 判断行为是否因为动物内因的困难而无法进行
    @abstractmethod
    def judge_action_validity(self, *paras):
        pass

    # 执行一类动作的成本 能量消耗
    @abstractmethod
    def action_cost(self, *action):
        pass

    # 动作成功的影响
    @abstractmethod
    def action_interior_outcome(self, *action):
        pass

    """
        改变身体状态的工具函数
    """

    @abstractmethod
    def body_change(self, *changes):
        pass

    """
        改变身体属性的工具函数
    """

    @abstractmethod
    def body_attribute_change(self, *values):
        pass

    @abstractmethod
    def post_turn_change(self):
        pass

    @abstractmethod
    def die(self):
        pass
