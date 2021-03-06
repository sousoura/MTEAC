from world.entity.entity_import import *
from world.world_project.mesh_world.entity.creature.animal.mesh_animal import Mesh_animal

class Mouse(Mesh_animal, Food):
    # 物种属性
    feeding_habits = ["Grass", "Grassland", "Fruit"]
    swimming_ability = 6
    life_area = "terrestrial"

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Mouse, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                    gender, crawl_ability, speed, aggressivity)
        Food.__init__(self, 1)

    def die(self):
        return None
