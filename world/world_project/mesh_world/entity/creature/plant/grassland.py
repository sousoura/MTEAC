from world.entity.entity_import import *


class Grassland(Plant_cluster):
    def __init__(self, position):
        super(Grassland, self).__init__(position)

    def die(self):
        pass
