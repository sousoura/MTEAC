from world.entity.creature.animal.human.human import Human


class Human_being(Human):
    def __init__(self, position, life):
        super(Human, self).__init__(position, life)

    def move(self, new_position):
        self.position = new_position

    # 行为造成的内部影响
    def performing_an_act(self, command):
        # if command[0] == 'successful':
        #     if command[1][0] == 'go':
        #         if command[1][1] == 'down':
        #             self.position[1] += 1
        pass

    # 想出一个行为
    def devise_an_act(self, perception):
        def find_running_direction(perception):
            direction = "down"
            if self.position[1] == len(perception[0]) - 1 and self.position[0] != 0:
                direction = "left"
            elif self.position[0] == 0 and self.position[1] != 0:
                direction = "up"
            elif self.position[1] == 0 and self.position[0] != len(perception[0][0]) - 1:
                direction = "right"
            elif self.position[0] == len(perception[0][0]) - 1 and self.position[1] != 0:
                direction = "down"
            for position in perception[1]:
                for creature in perception[1][position]:
                    if type(creature).__name__ == "Wolf":
                        delta_x = self.position[0] - creature.position[0]
                        delta_y = self.position[1] - creature.position[1]

                        if abs(delta_x) <= abs(delta_y):
                            if delta_x > 0:
                                direction = "right"
                            if delta_x <= 0:
                                direction = "left"
                        else:
                            if delta_y > 0:
                                direction = "down"
                            if delta_y <= 0:
                                direction = "up"

            return direction

        def get_command(word):
            return ['go', word]

        direction = find_running_direction(perception)
        return get_command(direction)

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
