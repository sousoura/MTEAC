from world.world_generator import World_generator
from world.mesh_world.world import Mesh_world as World
from world.mesh_world.state import Mesh_state as State


class Concrete_world_generator(World_generator):
    def generate_a_world(self, columns, rows, terrain_types_number):
        state = State(self.randomMatrix(columns, rows, terrain_types_number))
        return World(state)

    def randomMatrix(self, columns, rows, terrain_types_number):
        import random
        matrix = []
        for i in range(columns):
            matrix.append([])
            for j in range(rows):
                matrix[i].append(random.randrange(terrain_types_number))
        return matrix
