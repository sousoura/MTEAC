from world.entity.creature.animal.brain import Brain


class Mouse_brain(Brain):
    def devise_an_act(self, perception, self_information):
        """
           鼠鼠脑
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
                for animal in perception[1][position]:
                    if type(animal).__name__ == "Wolf":
                        delta_x = self_information.position[0] - animal.position[0]
                        delta_y = self_information.position[1] - animal.position[1]

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
