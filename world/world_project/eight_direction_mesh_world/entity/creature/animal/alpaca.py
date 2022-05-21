from world.entity.entity_import import *
from world.world_project.eight_direction_mesh_world.entity.obj.alpaca_corpse import Alpaca_corpse
from world.world_project.eight_direction_mesh_world.entity.creature.animal.eight_direction_mesh_animal \
    import Eight_direction_mesh_animal

"""
    草泥马 物种类
    方法用于物种的内部影响
"""


class Alpaca(Eight_direction_mesh_animal, Big_obj):
    # 物种属性
    feeding_habits = ["Grass", "Grassland", "Fruit"]
    swimming_ability = 4
    life_area = "terrestrial"

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Alpaca, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                     gender, crawl_ability, speed, aggressivity)

    # 得到感知
    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return [Alpaca_corpse(self.get_position(), 20)]
