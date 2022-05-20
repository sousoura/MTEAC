from world.entity.entity_import import *
from world.world_project.hexagonal_mesh_world.entity.obj.wolf_corpse import Wolf_corpse


"""
    狼类 物种类
    方法用于物种的内部影响
"""


class Wolf(Animal, Big_obj):
    # 物种属性
    feeding_habits = ["Human_being", "Human", "Alpaca", "Human_corpse", "Alpaca_corpse", "Mouse"]
    swimming_ability = 1
    life_area = "terrestrial"

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Wolf, self).__init__(position, life, brain, full_value, drinking_value, body_state, gender,
                                   crawl_ability, speed, aggressivity)

    # 得到感知
    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return [Wolf_corpse(self.get_position(), 20)]
