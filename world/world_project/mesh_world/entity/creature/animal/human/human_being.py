from world.entity.entity_import import *


"""
    人类类 物种类
    方法用于物种的行为的内部影响
"""


class Human_being(Human, Big_obj):
    # 物种属性
    feeding_habits = []
    swimming_ability = 4
    life_area = 0

    def __init__(self, position, life, brain, health_point, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Human, self).__init__(position, life, brain, health_point, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity)

    def move(self, new_position):
        self.position = new_position

    # 行为造成的内部影响
    def performing_an_act(self, command):
        # if command[0] == 'successful':
        #     if command[1][0] == 'go':
        #         if command[1][1] == 'down':
        #             self.position[1] += 1
        pass

    # 得到感知
    '''
        感知的结构： 整个是一个元组 其中：一个元组表示地形 另一个字典表示生物表
    '''
    def get_perception(self, landform_map, things_position):

        return tuple(landform_map), things_position

    def die(self):
        self.life = 0

    def is_die(self):
        return self.life <= 0
