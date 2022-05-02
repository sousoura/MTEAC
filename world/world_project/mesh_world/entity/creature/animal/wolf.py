from world.entity.entity_import import *


"""
    狼类 物种类
    方法用于物种的内部影响
"""


class Wolf(Animal, Big_obj):
    def __init__(self, position, life, brain):
        super(Wolf, self).__init__(position, life, brain)

    def move(self, new_position):
        self.position = new_position

    def eat(self, be_eator):
        pass

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
        self.life = 0

    def is_die(self):
        return self.life <= 0
