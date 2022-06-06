from world.world_generator import World_generator
"""
    here "pac_man_world"
"""
from world.world_project.pac_man_world.mods import *
from world.world_project.pac_man_world.entity.pac_man_entities import *


class Concrete_world_generator(World_generator):
    def generate_a_world(self):
        pass

    def generate_a_world_by_state(self):
        pass

    def default_generate_a_world(self):
        game_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    ]
        pac_man = Pac_man([1, 1])
        beans = [
            Bean([1, 2]),
            Bean([1, 3]),
            Bean([1, 4]),
            Bean([1, 5]),
            Bean([1, 6]),
            Bean([1, 7]),
            Bean([2, 1]),
            Bean([2, 1]),
            Bean([3, 1]),
            Bean([4, 1]),
            Bean([5, 1]),
            Bean([6, 1]),
            Bean([7, 1]),
            Bean([7, 1]),
            Bean([7, 2]),
            Bean([7, 3]),
            Bean([7, 4]),
                 ]
        ghosts = [
            Ghost([1, 7]),
            Ghost([7, 1]),
        ]
        return World(State(game_map, pac_man, beans, ghosts))
