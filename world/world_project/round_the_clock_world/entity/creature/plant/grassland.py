from world.entity.entity_import import *


class Grassland(Plant_cluster):
    def __init__(self, position, leaf_content=200):
        super(Grassland, self).__init__(position, leaf_content)

    def die(self):
        pass
