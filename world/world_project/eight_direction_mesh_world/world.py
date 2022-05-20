if __name__ == "main":
    import sys
    sys.path.append('../..')
    from world import World
else:
    from world.world import World


"""
    网格世界类
        状态类型为网格状态的世界
        规定世界如何推进
"""


class Eight_direction_mesh_world(World):
    play_mode = True
    backgroundable = False
    statistical = False

    def __init__(self, state):
        super(Eight_direction_mesh_world, self).__init__(state)

    def take_action(self, player_cmd=None):
        self.state.player_action(player_cmd)

    """
        规定世界调用哪些state方法来推进
    """
    # 地图推进一次
    def evolution(self):
        self.state.animal_action()
        self.state.plant_change()
        self.state.water_flow()
        # self.state.landform_evolution()

    def get_state(self):
        return self.state

    def get_openai_action_space_and_observation_space(self):
        from gym import spaces
        import numpy as np

        # 定义行动空间
        """
            1 - 14 对应 14个行为
            1 - 5 对应 5个方向
            对象选择属性取消 采取默认选择第一个的策略
        """
        direction_num = len(self.state.mteac_direction_list)
        action_space = spaces.Box(low=np.array([1, 1]), high=np.array([1, direction_num]), dtype=np.int64)

        """
            用六个数组表示感知
            前三个是地形
            第四个是实体
            当实体重合时只显示第一个实体
                实体类型映射为数字
        """

        # Define a 2-D observation space
        observation_shape = self.state.get_terrain_size()
        observation_shape = (observation_shape[1], observation_shape[0])
        observation_space = spaces.Tuple((
            spaces.Box(low=0,
                       high=self.state.maximum_height,
                       shape=observation_shape,
                       dtype=np.int64),
            spaces.Box(low=0,
                       high=self.state.maximum_height,
                       shape=observation_shape,
                       dtype=np.float16),
            spaces.Box(low=0,
                       high=self.state.terrain_range,
                       shape=observation_shape,
                       dtype=np.int64),
            spaces.Box(low=0,
                       high=self.state.entity_type_num - 1,
                       shape=observation_shape,
                       dtype=np.int64),
        )
        )

        return action_space, observation_space

    def translate_openai_command_to_mteac(self, mteac_state, openai_command):
        mteac_command = []

        mteac_command.append(mteac_state.mteac_command_list[openai_command[0] - 1])
        mteac_command.append(mteac_state.mteac_direction_list[openai_command[1] - 1])
        mteac_command.append(-1)

        return mteac_command

    def translate_mteac_state_to_openai(self, mteac_state):
        landform = mteac_state.get_landform_map()
        water_map = mteac_state.get_water_map()
        terrain_map = mteac_state.get_terrain_map()
        size = mteac_state.terrain_size
        entity_map = [[0 for i in range(size[1])][:] for p in range(size[0])]

        entity_types = mteac_state.entity_types[:]

        # animals = mteac_state.get_animals()
        # plants = mteac_state.get_plants()
        # objs = mteac_state.get_objects()

        for row_index in range(size[0]):
            for col_index in range(size[1]):
                if (row_index, col_index) not in mteac_state.get_animals_position() and \
                        (row_index, col_index) not in mteac_state.get_plants_position() and \
                        (row_index, col_index) not in mteac_state.get_objs_position():
                    continue
                position = (row_index, col_index)
                obj = mteac_state.get_entities_in_position(position)[:][0]
                entity_map[row_index][col_index] = entity_types.index(type(obj).__name__)

        return landform, water_map, terrain_map, entity_map

    """
                   统计数据 指定要统计的数据类型 筛选条件的分类 具体筛选条件（以数组形式）
                   数据类型：num, avg_life
                   筛选条件的分类，用哈夫曼编码：
                       物种为1;
                       生命值为2;
                       饥饿值为4;
                       位置为8.
                   具体筛选条件以物种、生命值、饥饿值、位置的顺序排序，如没有则不用填，其中生命值、饥饿值为具体数值，位置暂时留在这里，尚未开发
                   例如:
                       stat num 3 Human_being 5  为查询生命值为5的人类的个数
                       stat num 1 Human_being 为查询人类的个数
                """

    # 统计数据
    def statistics(self, cmd):
        str_to_print = None

        # 这里默认了所有世界都有生物
        creatures = self.state.animals + self.state.plants
        num = 0
        sum_life = 0
        for creature in creatures:
            pos = len(cmd) - 1
            if pos <= 0:
                str_to_print = "need more parameters, please try again"
                return str_to_print

            # 对于未死亡的生物，进行大量的筛选
            if not creature.is_die():
                if pos != 1:
                    cmd_num = int(cmd[2])
                else:
                    cmd_num = 0
                if cmd_num >= 8:
                    cmd_num -= 8
                    # 进行位置的相关筛选
                    pos -= 1
                if cmd_num >= 4:
                    cmd_num -= 4
                    # 进行饥饿值的相关筛选
                    pos -= 1
                if cmd_num >= 2:
                    cmd_num -= 2
                    # 进行生命值的相关筛选
                    if creature.life != int(cmd[pos]):
                        continue
                    pos -= 1
                if cmd_num >= 1:
                    cmd_num -= 1
                    # 进行物种的相关筛选
                    if type(creature).__name__ != cmd[pos]:
                        continue

            # 走到这里，就完成了筛选
            num += 1
            if cmd[1] == "avg_life":
                sum_life += creature.life

        # 完成了遍历
        if cmd[1] == "num":
            str_to_print = num
        elif cmd[1] == "avg_life":
            str_to_print = sum_life / num
        else:
            str_to_print = "wrong command,please input again"

        return str_to_print
