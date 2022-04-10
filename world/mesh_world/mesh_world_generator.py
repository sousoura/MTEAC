from world.world_generator import World_generator
from world.mesh_world.mesh_world import Mesh_world as World
from world.mesh_world.mesh_state import Mesh_state as State


class Concrete_world_generator(World_generator):
    def generate_a_world(self):
        state = State([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        return World(state)
