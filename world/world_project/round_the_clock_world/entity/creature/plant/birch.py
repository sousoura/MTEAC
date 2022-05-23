from world.entity.entity_import import *
from world.world_project.round_the_clock_world.entity.obj.fruit import Fruit
from world.world_project.round_the_clock_world.entity.obj.wood import Wood


class Birch(Plant):
    def __init__(self, position, leaf_content=50):
        super(Birch, self).__init__(position, leaf_content)

    def die(self):
        return [Wood(self.position[:]), Wood(self.position[:]), Wood(self.position[:])]

    def post_turn_change(self):
        import random
        random.seed(random.seed(self.get_id()))

        if random.randrange(1, 100) >= 99:
            return [Fruit(self.position, 1)]
