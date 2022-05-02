from world.entity.creature.creature import Creature
from abc import ABCMeta, abstractmethod


class Plant(Creature, metaclass=ABCMeta):
    pass
