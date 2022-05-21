from world.world_generator import World_generator
from world.world_project.blank_world.mods import *
from world.world_project.blank_world.entity.blank_entities import *


class Concrete_world_generator(World_generator):
    def generate_a_world(self):
        pass

    def generate_a_world_by_state(self):
        pass

    def default_generate_a_world(self):
        return World(State((10, 10)))
