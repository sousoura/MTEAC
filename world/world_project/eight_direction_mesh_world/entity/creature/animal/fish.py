from world.entity.entity_import import *


class Fish(Animal, Food):
    # 物种属性
    feeding_habits = ["Algae"]
    swimming_ability = 100
    life_area = "aquatic"  # 水生动物

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Fish, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                   gender, crawl_ability, speed, aggressivity)
        Food.__init__(self, 1)

    # 得到感知
    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return None
