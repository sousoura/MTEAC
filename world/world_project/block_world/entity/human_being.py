from world.entity.entity_import import *


class Human_being(Human):
    def __init__(self, position):
        super(Human_being, self).__init__(position)

    def move(self, new_position):
        self.position = new_position

    def action_cost(self, command):
        pass

    def judge_action_validity(self, state, player_cmd):
        new_position = state.position_and_direction_get_adjacent(self.get_position(), player_cmd)
        if new_position:
            if state.terrain[new_position[0]][new_position[1]] != 1:
                there_be_box = False
                for box in state.objs:
                    if box.get_position()[0] == new_position[0] and box.get_position()[1] == new_position[1]:
                        # 推到箱子
                        there_be_box = box
                        break
                if there_be_box:
                    box_position = there_be_box.get_position()
                    box_new_position = state.position_and_direction_get_adjacent(box_position, player_cmd)
                    if box_new_position:
                        if state.terrain[box_new_position[0]][box_new_position[1]] != 1:
                            # 判断是否和别的箱子碰撞
                            box_crash = False
                            for box in state.objs:
                                if box.get_position()[0] == box_new_position[0] and \
                                        box.get_position()[1] == box_new_position[1]:
                                    if box is not there_be_box:
                                        box_crash = True
                                        break
                            if not box_crash:
                                return True
                            else:
                                print("box crash")
                                return False
                        else:
                            print("box encounter obstacles")
                            return False
                    else:
                        print("cannot move out of the map")
                        return False
                else:
                    return True
            else:
                print("encounter obstacles")
                return False
        else:
            print("cannot move out of the map")
            return False

    def action_interior_outcome(self, state, player_cmd):
        new_position = state.position_and_direction_get_adjacent(self.get_position(), player_cmd)
        self.move(new_position)

    def body_attribute_change(self):
        pass

    def body_change(self):
        pass

    def die(self):
        pass

    def post_turn_change(self):
        pass
