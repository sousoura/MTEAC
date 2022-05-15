from world.entity.entity_import import *


class Grass(Plant):
    def __init__(self, position, leaf_content=10):
        super(Grass, self).__init__(position, leaf_content)

    def die(self):
        pass
