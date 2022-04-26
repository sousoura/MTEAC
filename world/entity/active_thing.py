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
    def performing_an_act(self, perception):
        pass

    @abstractmethod
    def devise_an_act(self, command):
        pass
