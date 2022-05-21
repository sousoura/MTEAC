from world.world_generator import World_generator
"""
    here "blank_world"
"""
from world.world_project.physics_world.mods import *
from world.world_project.physics_world.entity.physics_entities import *


class Concrete_world_generator(World_generator):
    def generate_a_world(self):
        pass

    def generate_a_world_by_state(self):
        pass

    def default_generate_a_world(self):
        return World(State())
