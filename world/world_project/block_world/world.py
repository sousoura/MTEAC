if __name__ == "main":
    import sys

    sys.path.append('../..')
    from world import World
    from world.world_project.block_world.entity.box import Box
else:
    from world.world import World
    from world.world_project.block_world.entity.box import Box


class Block_world(World):
    play_mode = True
    backgroundable = False
    statistical = False

    def __init__(self, state):
        super(Block_world, self).__init__(state)

    def take_action(self, player_cmd=None):
        if player_cmd:
            self.state.controled_huamn_action(player_cmd)

    """
        规定世界调用哪些state方法来推进
    """

    # 地图推进一次
    def evolution(self):
        pass

    def get_state(self):
        return self.state

    def get_openai_action_space_and_observation_space(self):
        from gym import spaces
        import numpy as np

        # 定义行动空间
        direction_num = len(self.state.mteac_direction_list)
        action_space = spaces.Discrete(4)

        # Define a 2-D observation space
        observation_shape = self.state.get_terrain_size()
        observation_shape = (observation_shape[1], observation_shape[0])
        observation_space = spaces.Tuple((spaces.Box(low=0,
                                                     high=1,
                                                     shape=observation_shape,
                                                     dtype=np.int64)
                                          ,
                                          spaces.Box(low=0,
                                                     high=1,
                                                     shape=observation_shape,
                                                     dtype=np.int64)
                                          ,
                                          ))

        return action_space, observation_space

    def translate_openai_command_to_mteac(self, mteac_state, openai_command):
        mteac_command = self.state.mteac_direction_list[openai_command]
        return mteac_command

    def translate_mteac_state_to_openai(self, mteac_state):
        def get_objs_map():
            objs_map = [[0 for i in range(mteac_state.terrain_size[1])][:] for n in range(mteac_state.terrain_size[0])]
            for obj in mteac_state.objs:
                if isinstance(obj, Box):
                    objs_map[obj.get_position()[0]][obj.get_position()[1]] = 1

            return objs_map

        openai_state = []
        openai_state.append(mteac_state.terrain)
        openai_state.append(get_objs_map())

        return openai_state

    # 统计数据
    def statistics(self, cmd):
        pass
