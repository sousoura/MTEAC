from world.entity.entity_import import *
from abc import ABCMeta, abstractmethod


class Container(metaclass=ABCMeta):
    # 可以放进空间的物品
    containable_objs = []

    def __init__(self):
        self.space = []

    def get_space(self):
        return self.space
