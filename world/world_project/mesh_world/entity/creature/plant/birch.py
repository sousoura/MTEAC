from world.entity.entity_import import *


class Birch(Plant):
    def __init__(self, position, leaf_content=50):
        super(Birch, self).__init__(position, leaf_content)

    def die(self):
        pass
