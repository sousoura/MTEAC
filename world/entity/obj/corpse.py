from world.entity.obj.food import Food
from world.entity.obj.obj import Obj
from abc import ABCMeta


class Corpse(Obj, Food, metaclass=ABCMeta):
    def __init__(self, position, size):
        Obj.__init__(self, position)
        Food.__init__(self, size)
