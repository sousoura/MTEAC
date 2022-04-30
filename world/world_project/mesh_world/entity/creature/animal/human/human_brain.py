from world.entity.creature.animal.brain import Brain


"""
    人脑 大脑类
"""


class Human_brain(Brain):
    def devise_an_act(self, perception, self_information):
        """
           人脑
       """
        def find_running_direction(perception):
            direction = "down"
            if self_information.position[1] == len(perception[0]) - 1 and self_information.position[0] != 0:
                direction = "left"
            elif self_information.position[0] == 0 and self_information.position[1] != 0:
                direction = "up"
            elif self_information.position[1] == 0 and self_information.position[0] != len(perception[0][0]) - 1:
                direction = "right"
            elif self_information.position[0] == len(perception[0][0]) - 1 and self_information.position[1] != 0:
                direction = "down"
            for position in perception[1]:
                for creature in perception[1][position]:
                    if type(creature).__name__ == "Wolf":
                        delta_x = self_information.position[0] - creature.position[0]
                        delta_y = self_information.position[1] - creature.position[1]

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
