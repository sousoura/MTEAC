from world.entity.entity_import import *


class Birch_wood(Plant_cluster, Big_obj):
    def __init__(self, position, leaf_content=500):
        super(Birch_wood, self).__init__(position, leaf_content)

    def die(self):
        pass
