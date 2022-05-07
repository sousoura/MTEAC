from world.entity.entity_import import *
from world.world_project.mesh_world.entity.obj.wolf_corpse import Wolf_corpse


"""
    狼类 物种类
    方法用于物种的内部影响
"""


class Wolf(Animal, Big_obj):
    # 物种属性
    feeding_habits = ["Human_being", "Human", "Alpaca", "Human_corpse", "Alpaca_corpse"]
    swimming_ability = 1
    life_area = 0

    def __init__(self, position, life, brain, health_point, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Wolf, self).__init__(position, life, brain, health_point, full_value, drinking_value, body_state, gender,
                                   crawl_ability, speed, aggressivity)

    # 行为造成的内部影响
    def performing_an_act(self, cmd):
        # if cmd[0] == 'successful':
        #     if cmd[1][0] == 'go':
        #         if cmd[1][1] == 'down':
        #             self.position[1] += 1
        pass

    # def devise_an_act(self, perception):
    #     return self.brain.devise_an_act(perception, self)

    # 得到感知
    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return Wolf_corpse(self.get_position(), 20)

    def is_die(self):
        return self.life <= 0
