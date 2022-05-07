from world.entity.obj.obj import Obj
from abc import ABCMeta, abstractmethod


class Food( metaclass=ABCMeta):
    def __init__(self, size):
        self.size = size

    def be_ate(self, eator):
        self.size -= eator.get_aggressivity() / 5
        if self.size <= 0:
            return True
        else:
            return False
