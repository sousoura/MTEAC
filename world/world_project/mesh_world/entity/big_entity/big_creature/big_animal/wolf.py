from world.entity.big_entity.big_creature.big_animal.big_animal import Big_animal


class Wolf(Big_animal):
    def __init__(self, position, life):
        super(Wolf, self).__init__(position, life)

    def move(self, new_position):
        self.position = new_position

    def eat(self):
        pass

    # 行为造成的内部影响
    def performing_an_act(self, cmd):
        if cmd[0] == 'successful':
            if cmd[1][0] == 'go':
                if cmd[1][1] == 'down':
                    self.position[1] += 1

    def devise_an_act(self, perception):
        def find_running_direction(perception):
            return "down"

        def get_command(word):
            return ['go', 'down']

        direction = find_running_direction(perception)
        return get_command(direction)

    # 得到感知
    def get_perception(self, terrain, things_position):
        return tuple(terrain), things_position
