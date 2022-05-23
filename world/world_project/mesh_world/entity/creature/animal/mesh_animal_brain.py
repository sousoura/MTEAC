from world.entity.creature.animal.brain import Brain


"""
    人脑 大脑类
"""


class Mesh_animal_brain(Brain):
    def devise_an_act(self, perception, self_information):
        """
           人脑
       """
        def find_running_direction(terrain_and_animal):
            direction = "down"
            if self_information.position[1] == len(terrain_and_animal[0]) - 1 and self_information.position[0] != 0:
                direction = "left"
            elif self_information.position[0] == 0 and self_information.position[1] != 0:
                direction = "up"
            elif self_information.position[1] == 0 and self_information.position[0] != len(terrain_and_animal[0][0]) - 1:
                direction = "right"
            elif self_information.position[0] == len(terrain_and_animal[0][0]) - 1 and self_information.position[1] != 0:
                direction = "down"
            for position in terrain_and_animal[1]:
                for animal in terrain_and_animal[1][position]:
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
                    break

            return direction

        def get_command(word):
            return ['go', word]

        terrain_and_animal = [perception.get_terrain_map(), perception.get_animals_position()]
        direction = find_running_direction(terrain_and_animal)
        return get_command(direction)
