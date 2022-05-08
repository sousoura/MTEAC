from world.entity.entity_import import *


class Fruit(Entity, Food):
    def __init__(self, position, size):
        super(Fruit, self).__init__(position)
        Food.__init__(self, size)
