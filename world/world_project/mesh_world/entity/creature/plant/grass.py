from world.entity.entity_import import *


class Grass(Plant):
    def __init__(self, position):
        super(Grass, self).__init__(position)

    def die(self):
        pass
