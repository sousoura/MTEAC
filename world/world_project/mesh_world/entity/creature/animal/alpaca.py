from world.entity.entity_import import *
from world.world_project.mesh_world.entity.obj.alpaca_corpse import Alpaca_corpse

"""
    草泥马 物种类
    方法用于物种的内部影响
"""


class Alpaca(Animal, Big_obj):
    # 物种属性
    feeding_habits = ["Grass", "Grassland"]
    swimming_ability = 4
    life_area = 0

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Alpaca, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                     gender, crawl_ability, speed, aggressivity)

    # 行为造成的内部影响
    def performing_an_act(self, cmd):
        # if cmd[0] == 'successful':
        #     if cmd[1][0] == 'go':
        #         if cmd[1][1] == 'down':
        #             self.position[1] += 1
        pass

    # 得到感知
    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return Alpaca_corpse(self.get_position(), 20)

    # 执行一类动作的成本 能量消耗
    def action_cost(self, action_type):
        action_type_num = self.action_list.index(action_type)
        self.action_cost_method_list[action_type_num](self)

    # 动作成功的影响
    def action_interior_outcome(self, action_type, parameter=None, obj=None, degree=None):
        pass
