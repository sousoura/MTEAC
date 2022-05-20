from world.entity.creature.animal.brain import Brain


"""
    狼这个物种的大脑 放ai的地方
"""


class Wolf_brain(Brain):
    def devise_an_act(self, perception, self_information):
        """
            狼脑
        """
        def find_running_direction(perception):
            direction = "left_up"
            if self_information.position[1] == len(perception[0]) - 1 and self_information.position[0] != 0:
                direction = "left"
            elif self_information.position[1] == 0 and self_information.position[0] != len(perception[0][0]) - 1:
                direction = "right"
            return direction

        def get_command(word):
            return ['go', word]

        direction = find_running_direction(perception)
        return get_command(direction)
