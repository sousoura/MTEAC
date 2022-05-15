from world.entity.entity_import import *
from abc import ABCMeta, abstractmethod


class Plant_cluster(Creature, metaclass=ABCMeta):
    def __init__(self, position, leaf_content=500, carapace=10):
        super().__init__(position, carapace)
        self.leaf_content = leaf_content

    def post_turn_change(self):
        pass
