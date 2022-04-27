from world.entity.big_entity.big_creature.big_animal.big_animal import Big_animal


class Wolf(Big_animal):
    def __init__(self, position, life):
        super(Wolf, self).__init__(position, life)

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
            return direction

        def get_command(word):
            return ['go', word]

        direction = find_running_direction(perception)
        return get_command(direction)

    # 得到感知
    def get_perception(self, terrain, things_position):
        return tuple(terrain), things_position

    def die(self):
        self.life = 0

    def is_die(self):
        return self.life <= 0
