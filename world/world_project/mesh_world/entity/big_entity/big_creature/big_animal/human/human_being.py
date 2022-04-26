from world.entity.big_entity.big_creature.big_animal.human.human import Human


class Human_being(Human):
    def __init__(self, position, life):
        super(Human, self).__init__(position, life)

    def move(self, new_position):
        self.position = new_position

    # 行为造成的内部影响
    def performing_an_act(self, command):
        if command[0] == 'successful':
            if command[1][0] == 'go':
                if command[1][1] == 'down':
                    self.position[1] += 1

    # 想出一个行为
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
