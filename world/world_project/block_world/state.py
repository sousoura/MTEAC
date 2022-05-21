# ctypes，用于python和c++的交互
import ctypes

if __name__ == "__main__":
    import sys
    import os

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
    config_path = CURRENT_DIR.rsplit('\\', 2)[0]  # 上三级目录
    sys.path.insert(0, config_path)
    from state import State
    from world.entity.entity_import import *
    from world.world_project.block_world.entity.block_entities import *
else:
    from world.state import State
    from world.entity.entity_import import *
    from world.world_project.block_world.entity.block_entities import *


class Block_state(State):

    mteac_direction_list = ["north", "south", "east", "west"]

    def __init__(self, terrain_size, terrain, subjects, objs):
        self.terrain_size = terrain_size
        self.terrain = terrain
        self.subjects = subjects
        self.objs = objs

    # 返回地图大小
    def get_terrain_size(self):
        return self.terrain_size

    def controled_huamn_action(self, player_cmd):
        controled_huamn = self.subjects[0]
        if isinstance(controled_huamn, Human_being):
            new_position = self.position_and_direction_get_adjacent(controled_huamn.get_position(), player_cmd)
            if new_position:
                there_be_box = False
                for box in self.objs:
                    if box.get_position()[0] == new_position[0] and box.get_position()[1] == new_position[1]:
                        # 推到箱子
                        there_be_box = box
                        break
                if there_be_box:
                    box_position = there_be_box.get_position()
                    box_new_position = self.position_and_direction_get_adjacent(box_position, player_cmd)
                    if box_new_position:
                        # 判断是否和别的箱子碰撞
                        box_crash = False
                        for box in self.objs:
                            if box.get_position()[0] == box_new_position[0] and \
                                    box.get_position()[1] == box_new_position[1]:
                                if box is not there_be_box:
                                    box_crash = True
                                    break
                        if not box_crash:
                            there_be_box.new_position(box_new_position)
                            controled_huamn.move(new_position)
                        else:
                            print("box crash")
                    else:
                        print("cannot move out of the map")
                else:
                    controled_huamn.move(new_position)
            else:
                print("cannot move out of the map")
        else:
            print("warning: the zero entity is not Human_being")

    def position_and_direction_get_adjacent(self, old_position, direction):
        if direction == 'east':
            if old_position[1] < self.terrain_size[1] - 1:
                return old_position[0], old_position[1] + 1
        elif direction == 'west':
            if old_position[1] > 0:
                return old_position[0], old_position[1] - 1
        elif direction == 'south':
            if old_position[0] < self.terrain_size[0] - 1:
                return old_position[0] + 1, old_position[1]
        elif direction == 'north':
            if old_position[0] > 0:
                return old_position[0] - 1, old_position[1]
        return False
