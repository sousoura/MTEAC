from world.world_generator import World_generator
from world.world_project.block_world.mods import *
from world.world_project.block_world.entity.block_entities import *
import random


class Concrete_world_generator(World_generator):
    def generate_a_world(self):
        pass

    def generate_a_world_by_state(self, state):
        return World(state)

    def default_generate_a_state(self):
        def default_generate_terrain(terrain_size):
            terrain = [[0 for i in range(terrain_size[1])][:] for n in range(terrain_size[0])]
            for i in range(5):
                terrain[random.randrange(0, terrain_size[0])][random.randrange(0, terrain_size[1])] = 1
            return terrain

        terrain_size = (50, 50)
        terrain = default_generate_terrain(terrain_size)
        subjects = []
        objs = []

        subjects.append(Human_being([3, 3]))
        objs.append(Box([5, 5]))
        objs.append(Box([6, 6]))

        return State(terrain_size, terrain, subjects, objs)

    def default_generate_a_world(self):
        return World(self.default_generate_a_state())
