from world.entity.entity_import import *
from world.world_project.mesh_world.entity.obj.wolf_corpse import Wolf_corpse
from world.world_project.mesh_world.entity.creature.animal.mesh_animal import Mesh_animal

"""
    狼类 物种类
    方法用于物种的内部影响
"""


class Wolf(Mesh_animal, Big_obj):
    # Attributes of species
    feeding_habits = ["Human_being", "Human", "Alpaca", "Human_corpse", "Alpaca_corpse", "Mouse"]
    swimming_ability = 1
    life_area = "terrestrial"

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Wolf, self).__init__(position, life, brain, full_value, drinking_value, body_state, gender,
                                   crawl_ability, speed, aggressivity)

    def die(self):
        return [Wolf_corpse(self.get_position(), 20)]
