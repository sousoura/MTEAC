from world.entity.creature.animal.brain import Brain


class Fish_brain(Brain):
    def devise_an_act(self, perception, self_information):
        """
           鱼脑
       """

        def find_running_direction(perception):
            direction = "left_up"
            if self_information.position[1] == len(perception[0]) - 1 and self_information.position[0] != 0:
                direction = "left"
            elif self_information.position[1] == 0 and self_information.position[0] != len(perception[0][0]) - 1:
                direction = "right"
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
                    break

            return direction

        def get_command(word):
            return ['go', word]

        direction = find_running_direction(perception)
        return get_command(direction)
