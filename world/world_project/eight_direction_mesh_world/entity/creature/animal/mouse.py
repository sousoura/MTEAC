from world.entity.entity_import import *


class Mouse(Animal, Food):
    # 物种属性
    feeding_habits = ["Grass", "Grassland", "Fruit"]
    swimming_ability = 6
    life_area = "terrestrial"

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Mouse, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                    gender, crawl_ability, speed, aggressivity)
        Food.__init__(self, 1)

    # 得到感知
    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return None
