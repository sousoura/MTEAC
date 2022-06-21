if __name__ == "main":
    import sys
    sys.path.append('../..')
    from world import World
else:
    from world.world import World


"""
    Mesh world class
        world class of Mesh_world world project
        It specifies how the world advances
"""


class Mesh_world(World):
    play_mode = True
    backgroundable = True
    statistical = True

    def __init__(self, state):
        super(Mesh_world, self).__init__(state)

    def take_action(self, player_cmd=None, ai_id=1):
        self.state.player_action(player_cmd, ai_id)
        return 0, False

    """
        Specifies which state functions the world calls to step the world
    """
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

        # define action space
        """
            1 - 14 correspond 14 actions
            1 - 5  correspond 5 directions
            No need select objects, always select the first object
        """
        direction_num = len(self.state.mteac_direction_list)
        action_space = spaces.Box(low=np.array([1, 1]), high=np.array([1, direction_num]), dtype=np.int64)

        """
            Represent perception with for arrays
             The first three are terrain
             The fourth is the entity
             Only show the first entity when the entities are coincident
                 Entity types are mapped to numbers
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
    statistical function
       instruction：num, avg_life
       Classification of filter conditions, encoded with Huffman code:
            species is 1;
            Life value is 2;
            Hunger value is 4;
            The position is 8.
       The specific filter conditions are sorted in the order of species, health value, hunger value, and location. If there is none, do not fill in. The health value and hunger value are specific values. The location is temporarily left here and has not yet been developed.
        E.g:
           stat num 3 Human_being 5
                Query the number of humans with a life value of 5
           stat num 1 Human_being
                Query the number of humans
    """

    def statistics(self, cmd):
        str_to_print = None

        creatures = self.state.animals + self.state.plants
        num = 0
        sum_life = 0
        for creature in creatures:
            pos = len(cmd) - 1
            if pos <= 0:
                str_to_print = "need more parameters, please try again"
                return str_to_print

            if not creature.is_die():
                if pos != 1:
                    cmd_num = int(cmd[2])
                else:
                    cmd_num = 0
                if cmd_num >= 8:
                    cmd_num -= 8
                    pos -= 1
                if cmd_num >= 4:
                    cmd_num -= 4
                    pos -= 1
                if cmd_num >= 2:
                    cmd_num -= 2
                    if creature.life != int(cmd[pos]):
                        continue
                    pos -= 1
                if cmd_num >= 1:
                    cmd_num -= 1
                    if type(creature).__name__ != cmd[pos]:
                        continue

            num += 1
            if cmd[1] == "avg_life":
                sum_life += creature.life

        if cmd[1] == "num":
            str_to_print = num
        elif cmd[1] == "avg_life":
            str_to_print = sum_life / num
        else:
            str_to_print = "wrong command,please input again"

        return str_to_print
