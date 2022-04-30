from abc import ABCMeta, abstractmethod


"""
    抽象的世界类
    不同的世界类型中有具体的世界类 会继承抽象的世界类
    世界具有状态属性和变化方法
        状态属性是状态类的实例 修改状态类可以改变世界的组成和变化规律
        变化方法规定了世界运行一次的变化
"""


# 抽象的世界类
class World(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def evolution(self):
        pass
