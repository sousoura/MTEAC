from world.entity.obj.obj import Obj
from abc import ABCMeta, abstractmethod


class Equipment(metaclass=ABCMeta):
    @abstractmethod
    def properties_gain(self, subject):
        pass
