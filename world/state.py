from abc import ABCMeta, abstractmethod


"""
    抽象的状态类
    由于状态类很自由 暂时并没有什么前置规定（以后发现了所有状态的共性可能会加些东西）
"""


# 抽象的状态类
class State(metaclass=ABCMeta):
    def __init__(self, terrain_size):
        self.terrain_size = terrain_size

    # 返回地图大小
    def get_terrain_size(self):
        return self.terrain_size
