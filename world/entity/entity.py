"""
    规定实体必须占据一个位置
"""


from abc import ABCMeta, abstractmethod
from world.entity.id_maker import Id_maker


class Entity(metaclass=ABCMeta):
    """
        编号生成器写在这里
    """
    id_maker = Id_maker()

    def __init__(self, position):
        self.position = position
        self.id = self.id_maker.make_id()

    def __str__(self):
        return type(self).__name__ + ": " + str(self.id)

    def get_position(self):
        return self.position

    def get_id(self):
        return self.id

    def is_id(self, in_id):
        return self.id == in_id

    def new_position(self, new_position):
        self.position = new_position
