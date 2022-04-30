from world.entity.creature.animal.human.human import Human


"""
    人类类 物种类
    方法用于物种的行为的内部影响
"""


class Human_being(Human):
    def __init__(self, position, life, brain):
        super(Human, self).__init__(position, life, brain)

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
    def get_perception(self, terrain, things_position):

        return tuple(terrain), things_position

    def die(self):
        self.life = 0

    def is_die(self):
        return self.life <= 0
