"""
    规定实体必须占据一个位置
"""


from abc import ABCMeta, abstractmethod


class Entity(metaclass=ABCMeta):
    """
        编号生成器写在这里
    """

    def __init__(self, position):
        self.position = position
        self.id = None

    def get_position(self):
        return self.position
