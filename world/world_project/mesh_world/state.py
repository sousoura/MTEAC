import random
# ctypes，用于python和c++的交互
import ctypes
# Used to convert multidimensional arrays to one-dimensional arrays
from itertools import chain

if __name__ == "__main__":
    import sys
    import os

    CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
    config_path = CURRENT_DIR.rsplit('\\', 2)[0]  # 上三级目录
    sys.path.insert(0, config_path)
    from state import State
else:
    from world.state import State
    from world.entity.entity_import import *
    from world.world_project.mesh_world.entity.mesh_entities import *

"""
    Mesh state
        Attributes：
            Terrain            A grid world of squares represented by a two-dimensional array
                landform_map(higjt and low)        The height of a grid is currently expressed as an integer
                water_map                          Water height in a certain place. Water will flow every turn
                terrain_map                        Specify whether a grid is mud or sand or stone or any terrain else
            Entity list
                Animal list
                Plant list
                Obj list

        Mesh world's functions are all about state modification or state reading
            The functions by which each attribute changes for a turn
                Animal action: animal_action and animal_act
                    animal move        moving_a_pace
                    animal eat          animal_eating
                    ...
                ...
            renew an attribute:
                renew_map
                ...
            functions for specifying spatial attributes
                function to specify what is "adjacent"   position_and_direction_get_adjacent
            ...
"""


class Mesh_state(State):
    # there are terrain_range+1 types of terrain
    terrain_range = 6
    # there are entity_type_num types of entity
    entity_type_num = 22

    mteac_command_list = ["go", "eat", "drink", "attack", "rest",
                          "pick_up", "put_down", "handling", "collect", "push",
                          "fabricate", "construct", "interaction", "use", ]

    mteac_direction_list = ["up", "down", "left", "right", "stay"]

    entity_types = ["Human_being", "Alpaca", "Fish", "Mouse", "Wolf", "Algae", "Birch", "Birch_wood", "Grass",
                    "Grassland", "Alpaca_corpse", "Axe", "Bucket", "Cart", "Crafting_table", "Door", "Fruit",
                    "Human_corpse", "Stone", "Wall", "Wolf_corpse", "Wood"]

    def __init__(self, maximum_height, landform_map, water_map, terrain_map, terrain_size, animals, plants, objects):
        # maps
        self.landform_map = landform_map
        self.water_map = water_map
        self.terrain_map = terrain_map

        # map attributes
        self.maximum_height = maximum_height
        self.terrain_size = terrain_size
        self.legal_direction = ["up", "down", "left", "right", "stay"]

        # entities
        self.animals = animals
        self.plants = plants
        self.objects = objects

        # position-entities dictionary
        self.animals_position = self.init_position_list(self.animals)
        self.plants_position = self.init_position_list(self.plants)
        self.objs_position = self.init_position_list(self.objects)

        # c++ code module
        CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
        config_path = CURRENT_DIR.rsplit('\\', 3)[0]  # 上三级目录

        dll_name = "MTEAC-C++.dll"
        self.pDll = ctypes.CDLL(config_path + "/c++/" + dll_name)
        self.Double_Len = ctypes.c_double * (self.terrain_size[0] * self.terrain_size[1])
        self.in_water_map = self.Double_Len()
        self.in_landform_map = self.Double_Len()

    """
        ***
            actions of animal
        ***
        input:  player_cmd：Player command, in array format [..., ..., ..., ...]
                By default, the first element is the action type, the second element is the action object, and the third element is the action parameter
            If the creature is judged to be controlled by the player(AI) it will use the player's commands otherwise it will use the commands returned by the brain
    """

    def player_action(self, player_cmd, ai_id):
        if not player_cmd:
            return

        player = self.get_entity_by_id(ai_id)

        if not player:
            print("Warning：Animal", ai_id, "does not exist or has dead.")
            return

        if not player.is_die():
            cmd = player_cmd
            # Operate according to instructions
            self.animal_action_command_analysis_and_execute(player, cmd)
            player.post_turn_change()

    # Renewal animal behavior
    # Animal movement in a round
    def animal_action(self):
        # Traversing creature list
        for animal in self.animals:
            # Determine whether the creature die
            if not animal.is_die():
                cmd = animal.devise_an_act(animal.get_perception(self))
                """
                    Determine if the object is a player and determine if there are commands
                """
                if animal.is_id(1):
                    continue
                # Operate according to command
                self.animal_action_command_analysis_and_execute(animal, cmd)
                animal.post_turn_change()
            else:
                self.creature_die(animal)
                del animal

    # Analyze the basic types of action commands and call the corresponding execution functions
    def animal_action_command_analysis_and_execute(self, animal, command):
        """
            If the action is legitimate, then the influence of the action will be produced
        """

        """
           Some actions are performed multiple times in a turn
        """
        def basic_act_number(animal, command):
            time = 1
            if command[0] == "go":
                time = animal.get_pace()
            return time

        """
            Judgment function of behavior legality
        """
        def judge_action_validity(animal, command):
            return animal.judge_action_validity(self, command)

        # Determine the number of times the action is performed(It's only greater than one when the animal is running)
        for time in range(int(basic_act_number(animal, command))):
            # The cost of attempting the action
            animal.action_cost(command[0])
            if judge_action_validity(animal, command):
                # If the action is valid, the action is executed
                self.animal_action_command_execute(animal, command)
            else:
                break

    # Execute commands to change the state of the world and creatures
    def animal_action_command_execute(self, animal, command):
        if command[0] == 'go':
            # walk
            self.moving_a_pace(animal, command[1])
        elif command[0] == 'eat':
            # eat
            self.animal_eating(animal, command[2])
        elif command[0] == 'drink':
            # drink
            self.animal_drinking(animal, command[1])
        elif command[0] == 'attack':
            # attack
            self.animal_attack(animal, command[2])
        elif command[0] == 'rest':
            # rest
            self.animal_rest(animal)

        # If the action is unique to humans
        elif isinstance(animal, Human):
            if command[0] in animal.action_list:
                # 人类行为
                self.human_action(animal, command)

    """
        Input   the animal instance and direction of movement
        Effect  If the move is legal, the move changes the creature's position state and updates the position-entities dictionary
    """
    def moving_a_pace(self, animal, direction):
        old_position = tuple(animal.get_position())
        new_position = self.position_and_direction_get_new_position(old_position, direction)

        # Impact of a successful move on the State instance
        self.change_animal_position(animal, old_position, new_position)
        # The effect of successful movement on the animal instance
        animal.action_interior_outcome(action_type="go", parameter=new_position)

    # old_position + direction = new_position
    def position_and_direction_get_new_position(self, old_position, direction):
        # Determine the legality and type of movement
        def judge_movement_legality(old_position, new_position):
            """
                determine whether movement is valid
            """
            if new_position:
                # Move up one space
                if self.landform_map[new_position[0]][new_position[1]] - \
                        self.landform_map[old_position[0]][old_position[1]] == 1:
                    return 2
                # Move down one space
                elif self.landform_map[new_position[0]][new_position[1]] - \
                        self.landform_map[old_position[0]][old_position[1]] == -1:
                    return -2
                # Move to a cell of the same height
                return True
            # The new position exceeds the map as an empty object
            return False

        if direction == 'stay':
            return tuple(old_position)

        # If it's on the left and right half-grid position
        if old_position[0] % 1 > 0:
            stride = 0.5
            if direction == 'down':
                if old_position[0] < self.terrain_size[0] - 1:
                    return old_position[0] + stride, old_position[1]
            elif direction == 'up':
                if old_position[0] > 0:
                    return old_position[0] - stride, old_position[1]
        # If it's on the up and down half-grid position
        elif old_position[1] % 1 > 0:
            stride = 0.5
            if direction == 'right':
                if old_position[1] < self.terrain_size[1] - 1:
                    return old_position[0], old_position[1] + stride
            elif direction == 'left':
                if old_position[1] > 0:
                    return old_position[0], old_position[1] - stride
        # If it is not on half grid position
        else:
            old_position = (int(old_position[0]), int(old_position[1]))
            adjacent = self.position_and_direction_get_adjacent(old_position, direction)
            # Move up
            kakusa = judge_movement_legality(old_position, adjacent)
            if kakusa == 2:
                return old_position[0] + (adjacent[0] - old_position[0]) * 0.5, \
                       old_position[1] + (adjacent[1] - old_position[1]) * 0.5
            # Move down
            elif kakusa == -2:
                return adjacent
            # Move to a cell of the same height
            elif kakusa:
                return adjacent

        print("accidental movement")
        return tuple(old_position)

    """
        eat action of animal
        input      the animal instance, direction, instance of what is eaten
    """

    def animal_eating(self, eator, be_eator):

        # Changes in the state of the eater instance and the instance of what is eaten
        eator.action_interior_outcome("eat", obj=be_eator)
        # If eaten, the victim disappears (dies)
        if be_eator.be_ate(eator):
            # map changes
            self.eliminate_exist_in_map(be_eator)
            del be_eator

    """
        animal drink
        input      the animal instance, direction
    """

    def animal_drinking(self, drinker, direction):
        drinker.action_interior_outcome("drink", parameter=direction)

    """
        animal attack
        input      the animal instance, the instance that was attacked
    """

    def animal_attack(self, attacker, be_attackeder):
        attacker.action_interior_outcome("attack", obj=be_attackeder)
        be_attackeder.be_attack(attacker.get_aggressivity())

        if be_attackeder.is_die():
            self.creature_die(be_attackeder)
            del be_attackeder

    # animal rest
    def animal_rest(self, rester):
        pass

    # human actions
    def human_action(self, human, command):
        def human_pick_up(state, human, obj):
            human.action_interior_outcome("pick_up", obj=obj)
            state.eliminate_exist_in_map(obj)

        def human_put_down(state, human, direction, obj):
            human.action_interior_outcome("put_down", obj=obj)
            new_position = state.position_and_direction_get_adjacent(human.get_position(), direction)
            state.add_exist_to_map(obj, new_position)
            obj.new_position(new_position)

        def human_construct(state, human, direction, objs):
            # create new entity
            new_position = self.position_and_direction_get_adjacent(human.get_position(), direction)[:]
            item_names = human.composed_table[names_orderly_tuplize(objs)]
            for item_name in item_names:
                self.add_exist_to_map(globals()[item_name](new_position))
            # Items disappear as costs
            human.action_interior_outcome("construct", obj=objs)
            for item in objs:
                if item in state.objects:
                    state.eliminate_exist_in_map(item)

        def human_collect_things(state, human, direction):
            gether_things = []

            # Get the position of collection place
            direction = command[1]
            direction_position = state.position_and_direction_get_adjacent(human.get_position(), direction)

            # Whether the collection place is forested
            if tuple(direction_position) in state.get_plants_position():
                for plant in state.get_plants_position()[tuple(direction_position)]:
                    if isinstance(plant, (Birch_wood,)):
                        gether_things.append(Wood(human.get_position()))
                        human.action_interior_outcome("collect", obj=gether_things)
                        return

            # Whether the collection place is collectable
            if direction_position:
                terrain_type = state.get_terrain_map()[int(direction_position[0])][int(direction_position[1])]
                thing_type = ["Stone", "Sandpile", "Soil_pile"][human.collectable.index(terrain_type)]

                """
                    To be supplemented: There are no barrel class yet, human can’t pick up sand and dirt
                """
                if thing_type == "Stone":
                    gether_things.append(Stone(human.get_position()))
                    human.action_interior_outcome("collect", obj=gether_things)
                    return
                else:
                    print("Sand and soil cannot be collected currently, this feature remain to be improved")

        def human_push(state, human, derection, obj):
            human_old_position = tuple(human.get_position())
            human_new_position = state.position_and_direction_get_new_position(human_old_position, derection)

            state.change_animal_position(human, human_old_position, human_new_position)
            human.action_interior_outcome(action_type="push", parameter=human_new_position)

            obj_old_position = tuple(obj.get_position())
            obj_new_position = state.position_and_direction_get_adjacent(obj_old_position, derection)

            if obj_new_position in state.objs_position:
                state.objs_position[obj_new_position].append(obj)
            else:
                state.objs_position[obj_new_position] = [obj]

            state.objs_position[obj_old_position].remove(obj)
            if len(state.objs_position[obj_old_position]) == 0:
                del state.objs_position[obj_old_position]

            obj.new_position(list(obj_new_position))

        if command[0] == "pick_up":
            human_pick_up(self, human, command[2])

        elif command[0] == "put_down":
            human_put_down(self, human, command[1], command[2])

        elif command[0] == "handling":
            human.action_interior_outcome("handling", obj=command[2])

        elif command[0] == "fabricate":
            human.action_interior_outcome("fabricate", obj=command[2])

        elif command[0] == "construct":
            human_construct(self, human, command[1], command[2])

        elif command[0] == "collect":
            human_collect_things(self, human, command[1])

        elif command[0] == "push":
            human_push(self, human, command[1], command[2])

    """
        ***
            update to the water map
        ***
    """
    # double * c_water_flow(int terrain_row, int terrain_col, double * in_water_map, double * in_landform_map, char * in_legal_direction)

    def water_flow(self):
        # Data initialization

        legal_direction = ctypes.c_char_p()
        for y in range(0, self.terrain_size[0]):
            for x in range(0, self.terrain_size[1]):
                self.in_water_map[y * self.terrain_size[1] + x] = self.water_map[y][x]
                self.in_landform_map[y * self.terrain_size[1] + x] = self.landform_map[y][x]


        legal_str = "\n".join(self.legal_direction)
        legal_str += "\0"
        legal_direction.value = legal_str.encode("utf-8")

        # for char in legal_direction.value:
        #     print(char)


        self.pDll.c_water_flow.restype = ctypes.POINTER(ctypes.c_double)
        # C ++ code returns a water map in the form of a one -dimensional array
        # s = input("input 312312312s1")
        map_array = self.pDll.c_water_flow(self.terrain_size[0], self.terrain_size[1],
                                      self.in_water_map, self.in_landform_map, legal_direction)
        # for num in map_array:
        #     print(num,end=" ")
        # print(" ")
        # print(map_array)

        # self.water_map = []
        for y in range(0, self.terrain_size[0]):
            for x in range(0, self.terrain_size[1]):
                self.water_map[y][x] = (map_array[x + y * self.terrain_size[1]])

    def water_flow_old(self):
        # Traversing water map
        for row_index in range(self.terrain_size[0]):
            for col_index in range(self.terrain_size[1]):
                # If its relative water height is less than 0.1, it is absorbed by the land
                if self.water_map[row_index][col_index] < 0.1:
                    self.water_map[row_index][col_index] = 0
                    continue

                # Get absolute water high
                absolute_water_high = self.water_map[row_index][col_index] + self.landform_map[row_index][col_index]
                land_high = self.landform_map[row_index][col_index]

                # Get the positions of adjacent cells in all legal directions
                """
                    The data structure of the position is determined by the data structure of the input position
                    so this is (row index, col index)
                """
                adjacent_positions = []
                for direction in self.legal_direction:
                    adjacent_position = self.position_and_direction_get_adjacent((row_index, col_index), direction)
                    if adjacent_position:
                        adjacent_positions. \
                            append(adjacent_position)

                # Determine absolute water height in all legal directions and reserve only the flowable position
                """
                    Data structure here: {position: absolute water height}
                """
                adjacent_absolute_water_highs = {}
                sum_absolute_water_high = absolute_water_high

                for adjacent_position in adjacent_positions:
                    adjacent_absolute_water_high = \
                        self.water_map[adjacent_position[0]][adjacent_position[1]] + \
                        self.landform_map[adjacent_position[0]][adjacent_position[1]]
                    # Keep only the lower ones because the water goes down
                    if adjacent_absolute_water_high < absolute_water_high:
                        adjacent_absolute_water_highs[adjacent_position] = adjacent_absolute_water_high
                        sum_absolute_water_high += adjacent_absolute_water_high

                # If all sides are higher, the water does not flow
                if len(adjacent_absolute_water_highs) == 0:
                    continue

                # get mean value
                avg_absolute_water_high = sum_absolute_water_high / (len(adjacent_absolute_water_highs) + 1)

                if avg_absolute_water_high < self.landform_map[row_index][col_index]:
                    water_amount = self.water_map[row_index][col_index]
                    self.water_map[row_index][col_index] = 0

                    adjacent_drop_highs = {}
                    sum_drop_high = 0

                    for position in adjacent_absolute_water_highs:
                        drop_high = land_high - adjacent_absolute_water_highs[position]
                        if drop_high > 0:
                            sum_drop_high += drop_high
                            adjacent_drop_highs[position] = drop_high

                    adjacent_drop_highs = sorted(adjacent_drop_highs.items(), key=lambda d: d[1], reverse=False)
                    drop_highs = tuple([i[1] for i in adjacent_drop_highs])
                    drop_num = len(adjacent_drop_highs)

                    for step in range(len(adjacent_drop_highs)):
                        if water_amount < sum(drop_highs[:step + 1]):
                            for ind in range(step - 1):
                                position = adjacent_drop_highs[ind][0]
                                self.water_map[position[0]][position[1]] += drop_highs[ind]
                                water_amount -= drop_highs[ind]
                            position = adjacent_drop_highs[step - 1][0]
                            self.water_map[position[0]][position[1]] += water_amount
                            break

                # If it could just take the average
                else:
                    self.water_map[row_index][col_index] += \
                        round(max(avg_absolute_water_high - absolute_water_high,
                                  - self.water_map[row_index][col_index]), 3)

                    self.water_map[row_index][col_index] = \
                        round(self.water_map[row_index][col_index], 3)

                    for position in adjacent_absolute_water_highs:
                        self.water_map[position[0]][position[1]] += \
                            max(avg_absolute_water_high -
                                self.water_map[position[0]][position[1]] -
                                self.landform_map[position[0]][position[1]],
                                -self.water_map[position[0]][position[1]])
                        self.water_map[position[0]][position[1]] = round(self.water_map[position[0]][position[1]], 3)

    # The concept of adjacency is defined here
    '''
        The input old coordinates cannot be on the half grid
    '''

    def position_and_direction_get_adjacent(self, old_position, direction):
        if direction == "stay":
            return old_position
        if direction == 'right':
            if old_position[1] < self.terrain_size[1] - 1:
                return old_position[0], old_position[1] + 1
        elif direction == 'left':
            if old_position[1] > 0:
                return old_position[0], old_position[1] - 1
        elif direction == 'down':
            if old_position[0] < self.terrain_size[0] - 1:
                return old_position[0] + 1, old_position[1]
        elif direction == 'up':
            if old_position[0] > 0:
                return old_position[0] - 1, old_position[1]
        return False

    def get_landform_map(self):
        return self.landform_map[:]

    def get_terrain_size(self):
        return self.terrain_size

    def get_water_map(self):
        return self.water_map[:]

    def get_terrain_map(self):
        return self.terrain_map[:]

    def get_animals(self):
        return self.animals

    def get_plants(self):
        return self.plants

    def get_objects(self):
        return self.objects

    def get_animals_position(self):
        return self.animals_position

    def get_plants_position(self):
        return self.plants_position

    def get_creatures_position(self):
        creatures_position = {}
        for position in self.animals_position:
            if position in self.plants_position:
                creatures_position[position] = self.animals_position[position] + self.plants_position[position]
            else:
                creatures_position[position] = self.animals_position[position]

        for position in self.plants_position:
            if position not in self.animals_position:
                creatures_position[position] = self.plants_position[position]
        return creatures_position

    def get_objs_position(self):
        return self.objs_position

    def get_entities_in_position(self, position):
        entities = []
        if position in self.animals_position:
            entities += self.animals_position[position]
        if position in self.plants_position:
            entities += self.plants_position[position]
        if position in self.objs_position:
            entities += self.objs_position[position]
        return entities

    def get_entity_by_id(self, id):
        for animal in self.animals:
            if animal.get_id() == id:
                return animal

        for plant in self.plants:
            if plant.get_id() == id:
                return plant

        for obj in self.objects:
            if obj.get_id() == id:
                return obj

        return False

    def renew_map(self, new_map):
        self.landform_map = new_map

    def eliminate_exist_in_map(self, entity):
        entity_position_list, entity_list = self.determine_entities_category(entity)

        if entity_position_list != -1:
            entity_position_list[tuple(entity.get_position())].remove(entity)
            entity_list.remove(entity)
            if len(entity_position_list[tuple(entity.get_position())]) == 0:
                del entity_position_list[tuple(entity.get_position())]
            del entity

    def add_exist_to_map(self, entity, position=None):
        entity_position_list, entity_list = self.determine_entities_category(entity)
        if not position:
            die_position = tuple(entity.get_position())
        else:
            die_position = tuple(position)

        if entity_position_list != -1:
            entity_list.append(entity)
            if die_position in entity_position_list:
                entity_position_list[die_position].append(entity)
            else:
                entity_position_list[die_position] = [entity]

    def determine_entities_category(self, entity):
        entity_position_list = -1
        entity_list = -1

        if isinstance(entity, Animal):
            entity_position_list = self.animals_position
            entity_list = self.animals
        elif isinstance(entity, Plant):
            entity_position_list = self.plants_position
            entity_list = self.plants
        elif isinstance(entity, Obj):
            entity_position_list = self.objs_position
            entity_list = self.objects

        return entity_position_list, entity_list

    def change_animal_position(self, animal, old_position, new_position):
        if new_position in self.animals_position:
            self.animals_position[new_position].append(animal)
        else:
            self.animals_position[new_position] = [animal]

        self.animals_position[old_position].remove(animal)
        if len(self.animals_position[old_position]) == 0:
            del self.animals_position[old_position]
        # animal.move(new_position)

    def creature_die(self, creature):
        die_position = tuple(creature.get_position())
        corpse = creature.die()
        if corpse:
            for remain in corpse:
                self.add_exist_to_map(remain)

        self.eliminate_exist_in_map(creature)

    def init_position_list(self, entity_list):
        things_position = {}
        for entity in entity_list:
            if tuple(entity.get_position()) in things_position:
                things_position[tuple(entity.get_position())].append(entity)
            else:
                things_position[tuple(entity.get_position())] = [entity]
        return things_position

    def plant_change(self):
        for plant in self.plants:
            products = plant.post_turn_change()
            if products:
                for product in products:
                    self.add_exist_to_map(product)


def names_orderly_tuplize(objs_list):
    def get_onj_name(obj):
        return type(obj).__name__

    objs_name_list = [get_onj_name(obj) for obj in objs_list]
    objs_name_list.sort()
    return tuple(objs_name_list)


# The following code was used as a test and can be ignored
if __name__ == "__main__":
    landform_map = [
        [5, 5, 5, 5, 5],
        [5, 1, 1, 1, 5],
        [5, 1, 1, 1, 5],
        [5, 1, 1, 1, 5],
        [5, 5, 5, 5, 5],
    ]
    water_map = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    terrain_map = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    terrain_size = (5, 5)
    maximum_height = 30
    animals = []
    plants = []
    objects = []
    state = Mesh_state(maximum_height, landform_map, water_map, terrain_map, terrain_size, animals, plants, objects)
    print(1)
    for line in state.get_water_map():
        print(line)
    input()
    while True:
        state.water_flow()
        # state.water_flow_old()
        for line in state.get_water_map():
            print(line)
        input()
