if __name__ == "__main__":
    import sys
    import os

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
    config_path = CURRENT_DIR.rsplit('\\', 6)[0]  # 上五级目录
    sys.path.insert(0, config_path)

    from world.entity.entity_import import *
    from world.world_project.mesh_world.entity.obj.alpaca_corpse import Alpaca_corpse
    from world.world_project.mesh_world.entity.creature.animal.mesh_animal import Mesh_animal

    from world.world_project.mesh_world.entity.creature.animal.alpaca_brain import Alpaca_brain
else:
    # from world.state import State
    from world.entity.entity_import import *
    from world.world_project.mesh_world.entity.mesh_entities import *

    from world.entity.entity_import import *
    from world.world_project.mesh_world.entity.obj.alpaca_corpse import Alpaca_corpse
    from world.world_project.mesh_world.entity.creature.animal.mesh_animal import Mesh_animal

import math
"""
    草泥马 物种类
    方法用于物种的内部影响
"""


class Alpaca(Mesh_animal, Big_obj):
    # 物种属性
    feeding_habits = ["Grass", "Grassland", "Fruit"]
    swimming_ability = 4
    life_area = "terrestrial"

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Alpaca, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                     gender, crawl_ability, speed, aggressivity)

    def die(self):
        return [Alpaca_corpse(self.get_position(), 20)]


if __name__ == "__main__":
    def print_state(state):
        def print_mesh_map(mesh_map):
            for line in mesh_map:
                print(line)
            print()

        landform_map = state.get_landform_map()
        water_map = state.get_water_map()
        terrain_map = state.get_terrain_map()

        animals_position = state.get_animals_position()
        plants_position = state.get_plants_position()
        objs_position = state.get_objs_position()

        print_mesh_map(landform_map)
        print_mesh_map(water_map)
        print_mesh_map(terrain_map)

        print(animals_position)
        print(plants_position)
        print(objs_position)

    position = [3, 3]
    life = 100
    brain = Alpaca_brain()
    full_value = 100
    drinking_value = 100
    body_state = "hao"
    gender = 1
    crawl_ability = 19
    speed = 19
    aggressivity = 19

    alpaca1 = Alpaca\
        (position, life, brain, full_value, drinking_value, body_state, gender, crawl_ability, speed, aggressivity)
    alpaca2 = Alpaca \
        (position, life, brain, full_value, drinking_value, body_state, gender, crawl_ability, speed, aggressivity)
    alpaca3 = Alpaca \
        (position, life, brain, full_value, drinking_value, body_state, gender, crawl_ability, speed, aggressivity)

    landform_map = [
        [5, 5, 5, 5, 5],
        [5, 1, 1, 1, 5],
        [5, 1, 1, 1, 5],
        [5, 1, 1, 1, 5],
        [5, 5, 5, 5, 5],
    ]
    water_map = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    terrain_map = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    maximum_height = 30
    terrain_size = (5, 5)
    animals = [alpaca2, alpaca3]
    plants = []
    objects = []
    from world.world_project.mesh_world.state import Mesh_state
    state = Mesh_state(maximum_height, landform_map, water_map, terrain_map, terrain_size, animals, plants, objects)

    alpaca1.get_perception(state)

    perception_state = alpaca1.get_perception(state)
    print_state(perception_state)
