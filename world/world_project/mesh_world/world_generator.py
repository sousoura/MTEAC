import random
import math

from world.world_generator import World_generator
from world.world_project.mesh_world.mods import *
from world.world_project.mesh_world.entity.mesh_entities import *

"""
    World generator of Mesh_world
        Used to initialize the world, or generate an instance of the world or state
"""

"""
    attention:
         When representing the coordinates of a 2D array
             If position is (row_index, column_index)
                 row_index represents the number of rows where it is as the ordinate
                 column_index represents the number of columns where it is located as the abscissa
"""


# World generator class for mesh world
class Concrete_world_generator(World_generator):

    def generate_a_world(self, maximum_height, map_size, landform_para, water_para, terrain_para,
                         animals_para, plants_para, obj_para):
        state = self.generate_a_state(maximum_height, map_size, landform_para, water_para, terrain_para,
                                      animals_para, plants_para, obj_para)
        print("The world map's parameters are:", "maximum height:", maximum_height, "map size:", map_size)
        return World(state)

    def generate_a_state(self, maximum_height, terrain_size, landform_para, water_para, terrain_para,
                         animals_para, plants_para, obj_para):

        """
            Define adjacency and prevent out of bounds
             row_index is the number of rows
             col_index is the number of columns
        """
        def define_adjacent(row_index, col_index):
            left = col_index - 1
            if left < 0:
                left = 0

            right = col_index + 1
            if right >= terrain_size[1]:
                right = terrain_size[1] - 1

            up = row_index - 1
            if up < 0:
                up = 0

            down = row_index + 1
            if down >= terrain_size[0]:
                down = terrain_size[0] - 1

            return left, right, up, down

        """ Randomly generate a grid world of a specific size """

        def randomMatrix(maximum_height, columns, rows):
            import random
            matrix = []
            for i in range(rows):
                matrix.append([])
                for j in range(columns):
                    matrix[i].append(random.randrange(maximum_height))
            return matrix

        """
            Find the location of peaks, valleys and pits and generate a map
        """

        def generate_landform_map(landform_para, maximum_height, rows, columns,
                                  peaks_para=None, mountains_para=None, valleys_para=None, pits_para=None):
            """
                The function wants to create a two-dimensional array of height_map The structure like [[1, 4, 6, ...], [12, 5, 6, ...], ...]
                where the number at each position represents the height at the position

                When landform_para == "default_landform", the default generation method is adopted
                No other generation methods have been defined yet
            """

            import random
            from world.world_project.mesh_world.landform import Peak
            # from world.world_project.mesh_world.landform import Pit

            # default land height
            normal_land_height = 3
            print("\tThe default land height is:", normal_land_height)

            # generate a completely flat world
            height_map = [[normal_land_height for i in range(columns)][:] for m in range(rows)]

            if landform_para == "default_landform":
                # generate peaks
                if not peaks_para:
                    peaks = []
                    # Determine the number of peaks, the more peaks it has, the more it is closer to the hills and the less it has, the more it is closer to the plains
                    peaks_num = max(int(math.log(columns * rows, 2)), 1)
                    print("\tpeaks number is:", peaks_num)
                    # peaks_num = 1

                    # Generate peaks randomly
                    # Peaks have the following attributes: peak value, surface size, slope, range
                    Peak.init_random_seed(12456)
                    Peak.init_map_size((rows, columns))
                    Peak.init_high_range((2, (maximum_height - normal_land_height - 2) ** 0.5))
                    for peak_id in range(peaks_num):
                        peaks.append(Peak.init_new_landform())

                # Generate pits
                # The method is not complete yet
                if not pits_para:
                    pits = []

                for row_index in range(rows):
                    for column_index in range(columns):
                        affect_sum = 0
                        for peak in peaks:
                            affect_sum += peak.affect((row_index, column_index))
                        height_map[row_index][column_index] += int(affect_sum)
                        height_map[row_index][column_index] = min(height_map[row_index][column_index], maximum_height)

            return height_map

        # generate water map
        def generate_water_map(water_para, landform_map):
            water_map = [[0 for a in range(terrain_size[1])] for i in range(terrain_size[0])]
            if water_para == "default_water":
                for row_index in range(terrain_size[0]):
                    for column_index in range(terrain_size[1]):
                        if landform_map[row_index][column_index] <= maximum_height / 1.2:
                            water_map[row_index][column_index] = 2

            builder_state = \
                self.building_a_state(maximum_height, landform_map, water_map,
                                      [[0 for a in range(terrain_size[1])] for b in range(terrain_size[0])],
                                      terrain_size, [], [], [])
            import time as Time
            start = Time.time()
            print("\tStart water flow rehearsal")
            for time in range(500):
                print("\tPerform the", time, "water rehearsal")
                builder_state.water_flow()
                # builder_state.water_flow_old()
            print("\twater rehearsal is complete")
            end = Time.time()
            print(end - start)

            return builder_state.get_water_map()

        # 生成地貌地圖
        def generate_terrain_map(terrain_para, landform_map, water_map):
            terrain_map = [[3 for a in range(terrain_size[1])] for i in range(terrain_size[0])]
            if terrain_para == "default_terrain":
                for row_index in range(terrain_size[0]):
                    for column_index in range(terrain_size[1]):
                        # Wetland generated
                        """
                            deep water is the water bottom
                            Shallow water is a swamp
                            Wet places are wetland/mud
                        """
                        # All places have a small chance to generate rocky land
                        # 99% chance not to generate rocky land

                        """
                            Define adjacency and prevent out of bounds
                        """
                        left, right, up, down = define_adjacent(row_index=row_index, col_index=column_index)

                        if random.randrange(0, maximum_height * 700) > landform_map[row_index][column_index]:
                            if water_map[row_index][column_index] >= 2:
                                terrain_map[row_index][column_index] = 6
                                # Where there is a lot of water, there is a certain probability of generating broken ground
                                if random.randrange(1, 1000) > 998:
                                    terrain_map[row_index][column_index] = 1
                                    terrain_map[up][column_index] = 1
                                    terrain_map[row_index][down] = 1
                                    terrain_map[up][down] = 1
                                    terrain_map[down][column_index] = 1
                                    terrain_map[row_index][right] = 1
                                    terrain_map[down][right] = 1
                                    terrain_map[down][down] = 1
                                    terrain_map[up][right] = 1
                            elif water_map[row_index][column_index] >= 1:
                                terrain_map[row_index][column_index] = 5
                            elif water_map[row_index][column_index] > 0.1:
                                terrain_map[row_index][column_index] = 4
                            else:
                                if random.randrange(1, 1000) >= 999:
                                    terrain_map[row_index][column_index] = 2
                            # Randomly generated sand
                        # Generate rocky land
                        else:
                            if random.randrange(1, 12) > 2:
                                terrain_map[row_index][column_index] = 0
                                terrain_map[up][column_index] = 0
                                terrain_map[row_index][left] = 0
                                terrain_map[up][left] = 0
                                terrain_map[down][column_index] = 0
                                terrain_map[row_index][right] = 0
                                terrain_map[down][right] = 0
                                terrain_map[down][left] = 0
                                terrain_map[up][right] = 0
                            else:
                                terrain_map[row_index][column_index] = 1
                                terrain_map[up][column_index] = 1
                                terrain_map[row_index][left] = 1
                                terrain_map[up][left] = 1
                                terrain_map[down][column_index] = 1
                                terrain_map[row_index][right] = 1
                                terrain_map[down][right] = 1
                                terrain_map[down][left] = 1
                                terrain_map[up][right] = 1

            # print()
            # for line in terrain_map:
            #     print(line)

            return terrain_map

        def generate_animals(animals_para):
            animals_list = []

            ''' If no specific parameters are given, the default generation method is used '''
            if animals_para == "random_animals":
                random_animals(animals_list)

            else:
                pass

            return animals_list

        # 生成動物
        def random_animals(animal_list):
            animal_list.append(Human_being(position=[3, 3], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0, gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Human_being(position=[3, 4], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0,
                                           gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Wolf(position=[1, 15], life=100, brain=Wolf_brain(),
                                    full_value=70, drinking_value=70, body_state=0, gender=True,
                                    crawl_ability=1, speed=2, aggressivity=50
                                    ))
            animal_list.append(Alpaca(position=[10, 10], life=100, brain=Alpaca_brain(),
                                      full_value=70, drinking_value=70, body_state=0,
                                      gender=True,
                                      crawl_ability=4, speed=1, aggressivity=5
                                      ))
            animal_list.append(Wolf(position=[1, 3], life=100, brain=Wolf_brain(),
                                    full_value=70, drinking_value=70, body_state=0, gender=True,
                                    crawl_ability=1, speed=2, aggressivity=50
                                    ))
            animal_list.append(Human_being(position=[3, 5], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0,
                                           gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Human_being(position=[2, 4], life=100, brain=Human_brain(),
                                           full_value=70, drinking_value=70, body_state=0,
                                           gender=True,
                                           crawl_ability=1, speed=2, aggressivity=50
                                           ))
            animal_list.append(Mouse(position=[10, 4], life=100, brain=Mouse_brain(),
                                     full_value=70, drinking_value=70, body_state=0,
                                     gender=True,
                                     crawl_ability=4, speed=1, aggressivity=5
                                     ))
            animal_list.append(Mouse(position=[2, 10], life=100, brain=Mouse_brain(),
                                     full_value=70, drinking_value=70, body_state=0,
                                     gender=True,
                                     crawl_ability=4, speed=1, aggressivity=5
                                     ))
            animal_list.append(Fish(position=[6, 45], life=100, brain=Fish_brain(),
                                    full_value=70, drinking_value=70, body_state=0,
                                    gender=True,
                                    crawl_ability=1, speed=1, aggressivity=5
                                    ))
            animal_list.append(Fish(position=[43, 45], life=100, brain=Fish_brain(),
                                    full_value=70, drinking_value=70, body_state=0,
                                    gender=True,
                                    crawl_ability=1, speed=1, aggressivity=5
                                    ))

        def generate_plants(plants_para, landform_map, water_map, terrain_map):
            plants_list = []

            if plants_para == "random_plants":
                for row_index in range(terrain_size[0]):
                    for col_index in range(terrain_size[1]):

                        left, right, up, down = define_adjacent(col_index=col_index, row_index=row_index)

                        # Weeds grow in deep water
                        if terrain_map[row_index][col_index] > 4:
                            if random.randrange(1, 10000) >= 9000:
                                plants_list.append(Algae((row_index, col_index)))
                        # Shallow water can grow both aquatic and grass
                        elif terrain_map[row_index][col_index] == 4:
                            if random.randrange(1, 10000) >= 9890:
                                plants_list.append(Algae((row_index, col_index)))
                            elif random.randrange(1, 10000) >= 9890:
                                plants_list.append(Grass((row_index, col_index)))
                        # Common land with long grass and trees
                        elif terrain_map[row_index][col_index] == 3:
                            # grass
                            if random.randrange(1, 10000) >= 9890:
                                plants_list.append(Grass((row_index, col_index)))
                            # grassland
                            elif random.randrange(1, 10000) >= 9900:
                                plants_list.append(Grassland((row_index, col_index)))

                                plants_list.append(Grass((up, col_index)))
                                plants_list.append(Grass((row_index, right)))
                                plants_list.append(Grass((down, col_index)))
                                plants_list.append(Grass((row_index, left)))
                                plants_list.append(Grass((up, left)))
                                plants_list.append(Grass((up, right)))
                                plants_list.append(Grass((down, right)))
                                plants_list.append(Grass((down, left)))
                            # tree
                            elif random.randrange(1, 10000) >= 9990:
                                plants_list.append(Birch((row_index, col_index)))
                            # tree wood
                            elif random.randrange(1, 10000) >= 9990:
                                plants_list.append(Birch_wood((row_index, col_index)))

                                plants_list.append(Birch((up, col_index)))
                                plants_list.append(Birch((row_index, right)))
                                plants_list.append(Birch((down, col_index)))
                                plants_list.append(Birch((row_index, left)))
                                plants_list.append(Birch((up, left)))
                                plants_list.append(Birch((up, right)))
                                plants_list.append(Birch((down, right)))
                                plants_list.append(Birch((down, left)))

            return plants_list

        # generate objs
        def generate_objs(obj_para):
            obj_list = []
            if obj_para == "random_obj":

                obj_list.append(Stone([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Wood([5, 5]))
                obj_list.append(Axe([5, 5]))
                obj_list.append(Cart([8, 8]))
            else:

                pass

            return obj_list

        # 生成地图
        print("generate landform map...")
        landform_map = generate_landform_map(landform_para, maximum_height, terrain_size[0], terrain_size[1])
        print("generate wate map...")
        water_map = generate_water_map(water_para, landform_map)
        print("generate terrain type map...")
        terrain_map = generate_terrain_map(terrain_para, landform_map, water_map)

        # generate entities
        print("generate animals...")
        animals_list = generate_animals(animals_para)
        print("generate plants...")
        plants_list = generate_plants(plants_para, landform_map, water_map, terrain_map)
        print("generate objs...")
        obj_list = generate_objs(obj_para)
        print("Status generation is complete！")

        return self.building_a_state(maximum_height, landform_map, water_map, terrain_map, terrain_size,
                                     animals_list, plants_list, obj_list)

    """
        Input property value as parameter to generate state
        return a State instance
    """

    # Build a world with existing information
    def building_a_state(self, maximum_height, landform_map, water_map, terrain_map, terrain_size, animals_list,
                         plants_list, obj_list):
        return State(maximum_height, landform_map, water_map, terrain_map, terrain_size, animals_list,
                     plants_list, obj_list)

    # Construct a world instance by state instance
    def generate_a_world_by_state(self, state):
        return World(state)

    def default_generate_a_world(self):
        return self.generate_a_world(maximum_height=30, map_size=(50, 100),
                                     animals_para="random_animals", plants_para="random_plants",
                                     obj_para="random_obj",
                                     water_para="default_water",
                                     landform_para="default_landform",
                                     terrain_para="default_terrain")
