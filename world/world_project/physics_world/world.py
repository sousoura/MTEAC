if __name__ == "main":
    import sys

    sys.path.append('../..')
    from world import World
else:
    from world.world import World


class Physics_world(World):
    play_mode = True
    backgroundable = False
    statistical = False

    def __init__(self, state):
        super(Physics_world, self).__init__(state)

    def take_action(self, player_cmd=(0, 0)):
        self.state.plater_ctrl(player_cmd)

    """
        规定世界调用哪些state方法来推进
    """

    # 地图推进一次
    def evolution(self):
        self.state.step()

    def get_state(self):
        return self.state

    def get_openai_action_space_and_observation_space(self):
        from gym import spaces
        import numpy as np

        # 定义行动空间
        # direction_num = len(self.state.mteac_direction_list)
        direction_num = (10, 10)
        action_space = spaces.Tuple((spaces.Discrete(10000), spaces.Discrete(10000)))

        # Define a 2-D observation space
        # observation_shape = self.state.get_terrain_size()
        observation_shape = (10, 10)
        observation_shape = (observation_shape[1], observation_shape[0])
        observation_space = spaces.Box(low=0,
                                       high=1,
                                       shape=observation_shape,
                                       dtype=np.int64)

        return action_space, observation_space

    def translate_openai_command_to_mteac(self, mteac_state, openai_command):
        mteac_command = []
        mteac_command.append(openai_command[0] - 5000)
        mteac_command.append(openai_command[1] - 5000)
        return mteac_command

    def translate_mteac_state_to_openai(self, mteac_state):
        pass
        return None

    # 统计数据
    def statistics(self, cmd):
        pass
