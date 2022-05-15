"""
    该接口用于规定可以运动的实体必须有一个运动和行为的函数的特性
"""


# 抽象类加抽象方法就等于面向对象编程中的接口
from abc import ABCMeta, abstractmethod


class Active_thing(metaclass=ABCMeta):  # 必须实现interface中的所有函数，否则会编译错误
    @abstractmethod
    def move(self, new_position):
        pass

    @abstractmethod
    def judge_action_validity(self, world_state, command):
        pass

    # 执行一类动作的成本 能量消耗
    @abstractmethod
    def action_cost(self, action_type):
        pass

    # 动作成功的影响
    @abstractmethod
    def action_interior_outcome(self, action_type, parameter=None, obj=None, degree=None):
        pass
