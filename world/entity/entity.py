"""
    规定实体必须占据一个位置
"""


from abc import ABCMeta, abstractmethod


class Entity(metaclass=ABCMeta):
    id = None

    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position
