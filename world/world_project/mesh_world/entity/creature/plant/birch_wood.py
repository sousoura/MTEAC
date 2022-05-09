from world.entity.entity_import import *
from world.world_project.mesh_world.entity.obj.fruit import Fruit


class Birch_wood(Plant_cluster, Big_obj):
    def __init__(self, position, leaf_content=500):
        super(Birch_wood, self).__init__(position, leaf_content)

    def die(self):
        pass

    def post_turn_change(self):
        import random
        random.seed(self.get_id())

        if random.randrange(1, 100) >= 99:
            return [Fruit(self.position, 1)]
