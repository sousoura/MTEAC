"""
    规定大实体不能和其它实体在同一个位置
"""

from world.entity.entity import Entity
from abc import ABCMeta, abstractmethod


class Big_entity(Entity, metaclass=ABCMeta):
    def __init__(self, position):
        super(Big_entity, self).__init__(position)
