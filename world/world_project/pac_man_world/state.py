# ctypes，用于python和c++的交互
import ctypes
import random

if __name__ == "__main__":
    import sys
    import os

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
    config_path = CURRENT_DIR.rsplit('\\', 2)[0]  # 上三级目录
    sys.path.insert(0, config_path)
    from state import State
    from world.entity.entity_import import *
    """
        here "pac_man_world"
    """
    from world.world_project.pac_man_world.entity.pac_man_entities import *
else:
    from world.state import State
    from world.entity.entity_import import *
    """
        here "pac_man_world"
    """
    from world.world_project.pac_man_world.entity.pac_man_entities import *


class Pac_man_state(State):

    def __init__(self, game_map, pac_man, beans, ghosts):
        self.game_map = game_map
        self.map_size = (len(game_map), len(game_map[0]))
        self.pac_man = pac_man
        self.beans = beans
        self.ghosts = ghosts

    def pac_man_action(self, player_cmd):
        # determines whether the movement condition is met and moves

        # move up
        if player_cmd == 1:
            new_position = (self.pac_man.get_position()[0] - 1, self.pac_man.get_position()[1])
            if not (new_position[0] < 0 or self.game_map[new_position[0]][new_position[1]] == 1):
                self.pac_man.new_position(list(new_position))
        # move down
        elif player_cmd == 2:
            new_position = (self.pac_man.get_position()[0] + 1, self.pac_man.get_position()[1])
            if not (new_position[0] >= self.map_size[0] or self.game_map[new_position[0]][new_position[1]] == 1):
                self.pac_man.new_position(list(new_position))
        # move left
        elif player_cmd == 3:
            new_position = (self.pac_man.get_position()[0], self.pac_man.get_position()[1] - 1)
            if not (new_position[0] < 0 or self.game_map[new_position[0]][new_position[1]] == 1):
                self.pac_man.new_position(list(new_position))
        # move right
        elif player_cmd == 4:
            new_position = (self.pac_man.get_position()[0], self.pac_man.get_position()[1] + 1)
            if not (new_position[0] >= self.map_size[1] or self.game_map[new_position[0]][new_position[1]] == 1):
                self.pac_man.new_position(list(new_position))

        else:
            return False

        for bean in self.beans:
            if new_position[0] == bean.get_position()[0] and new_position[1] == bean.get_position()[1]:
                self.beans.remove(bean)
                break

        if len(self.beans) == 0:
            return 1

    def ghosts_action(self):
        for ghost in self.ghosts:
            cmd = random.randrange(1, 5)

            # move up
            if cmd == 1:
                new_position = (ghost.get_position()[0] - 1, ghost.get_position()[1])
                if not (new_position[0] < 0 or self.game_map[new_position[0]][new_position[1]] == 1):
                    ghost.new_position(list(new_position))
            # move down
            elif cmd == 2:
                new_position = (ghost.get_position()[0] + 1, ghost.get_position()[1])
                if not (new_position[0] >= self.map_size[0] or self.game_map[new_position[0]][new_position[1]] == 1):
                    ghost.new_position(list(new_position))
            # move left
            elif cmd == 3:
                new_position = (ghost.get_position()[0], ghost.get_position()[1] - 1)
                if not (new_position[0] < 0 or self.game_map[new_position[0]][new_position[1]] == 1):
                    ghost.new_position(list(new_position))
            # move right
            elif cmd == 4:
                new_position = (ghost.get_position()[0], ghost.get_position()[1] + 1)
                if not (new_position[0] >= self.map_size[1] or self.game_map[new_position[0]][new_position[1]] == 1):
                    ghost.new_position(list(new_position))
            else:
                continue

            if new_position[0] == self.pac_man.get_position()[0] and new_position[1] == self.pac_man.get_position()[1]:
                return -1
