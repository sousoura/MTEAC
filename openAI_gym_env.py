from abc import ABCMeta, abstractmethod


class GymEnv(metaclass=ABCMeta):
    # 初始化环境
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    # 重置环境中所有基于状态的变量
    def reset(self):
        pass

    @abstractmethod
    # 给定一个动作，它会将我们的环境从一个状态转移到另一个状态
    def step(self, action):
        pass

    @abstractmethod
    # 可视化渲染
    def render(self):
        pass

    @abstractmethod
    # 设定随机种子
    def seed(self, seed=None):
        pass

    @abstractmethod
    # 关闭图形界面
    def close(self):
        pass


"""
    element的父类
"""


class Point(metaclass=ABCMeta):
    pass
