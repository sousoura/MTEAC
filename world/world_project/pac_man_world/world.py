if __name__ == "main":
    import sys

    sys.path.append('../..')
    from world import World
else:
    from world.world import World


class Pac_man_world(World):
    play_mode = False
    backgroundable = False
    statistical = False

    def __init__(self, state):
        super(Pac_man_world, self).__init__(state)

    # the specified entity executes the instruction
    def take_action(self, player_cmd=None, ai_id=1):
        # return reward and done
        return 0, self.state.pac_man_action(player_cmd)

    # the environment evolves in a turn
    def evolution(self):
        if self.state.ghosts_action() is not None:
            return [-1]

    def get_state(self):
        return self.state

    def get_openai_action_space_and_observation_space(self):
        from gym import spaces
        import numpy as np

        # define action space
        action_space = spaces.Discrete(4)

        # Define a 2-D observation space
        observation_shape = (9, 9)
        observation_shape = (observation_shape[1], observation_shape[0])
        observation_space = spaces.Box(low=0,
                                       high=1,
                                       shape=observation_shape,
                                       dtype=np.int64)

        return action_space, observation_space

    def translate_openai_command_to_mteac(self, mteac_state, openai_command):
        return openai_command

    def translate_mteac_state_to_openai(self, mteac_state):
        return mteac_state

    # 统计数据
    def statistics(self, cmd):
        pass
