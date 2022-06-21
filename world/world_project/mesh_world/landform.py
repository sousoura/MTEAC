from abc import ABCMeta, abstractmethod


"""
    Define high and low terrain using the method of Peak, Ridge, Pit, Valley
     The mountain is done, now going to do three more
         Note that all terrain types inherit Landform
"""


class Landform(metaclass=ABCMeta):
    map_size = (0, 0)

    def __init__(self, position, degree_value, slope, scope):
        self.position = position
        self.degree_value = degree_value
        self.slope = slope
        self.scope = scope

    @classmethod
    def init_new_landform(cls):
        pass

    @classmethod
    def init_map_size(cls, map_size):
        cls.map_size = map_size

    @classmethod
    def init_random_seed(cls, random_seed):
        cls.random.seed(random_seed)

    @abstractmethod
    def affect(self, point_position):
        pass


class Peak(Landform):
    peaks = []
    peaks_position = []
    peak_high_range = (2, 20)
    import random
    random = random
    random_seed = 1234
    random.seed(random_seed)

    def __init__(self, position, peak_value=None, peak_surface_size=None, slope=None, scope=None):
        super(Peak, self).__init__(position, peak_value, slope, scope)

        self.peak_surface_size = peak_surface_size

    @classmethod
    def init_new_landform(cls):
        position = True
        while position in cls.peaks_position or position is True:
            position = (cls.random.randrange(cls.map_size[0]), cls.random.randrange(cls.map_size[1]))

        peak_value = cls.random.randrange(cls.peak_high_range[0], cls.peak_high_range[1])
        peak_surface_size = cls.random.randrange(2, 5)

        slope = cls.random.random() * 0.05
        # slope = cls.random.random() * 0.7
        # When the effect is less than this value, the peak fails
        scope = 1

        cls.peaks_position.append(position)
        cls.peaks.append(Peak(position, peak_value, peak_surface_size, slope, scope))
        return cls.peaks[-1]

    def affect(self, point_position):
        # Calculate the distance from the point to the top of the mountain
        distance = (point_position[0] - self.position[0]) ** 2 + (point_position[1] - self.position[1]) ** 2
        # Calculate the effect of the mountain on the height of the point
        # Height of summit minus distance times steepness
        affect = self.degree_value - distance * self.slope
        # If the impact is negative or too small, cancel the impact
        # self.degree_value = 6
        if affect < self.scope:
            affect = 0
        # Returns the value of the effect
        return affect

    @classmethod
    def init_high_range(cls, high_range):
        cls.peak_high_range = high_range


class Pit(Landform):
    pits = []
    pits_position = []
    pit_low_range = (-3, -1)
    import random
    random = random
    random_seed = 114514
    random.seed(random_seed)

    def __init__(self, position, sub_value=None, pit_affect_size=None, slope=None, scope=None):
        super(Pit, self).__init__(position, sub_value, slope, scope)

        self.pit_affect_size = pit_affect_size

    """
        Define a trench by defining an initial point and flow direction
             The flow direction is a unit vector representing the weight of the probability generated in the next direction
             If the flow is down to the right, it won't go left or up
    """
    @classmethod
    def init_new_landform(cls):
        class Pit_point():
            pass

        def initial_position(flow_direction):
            position = (cls.map_size[0] - 1, cls.map_size[1] - 1)
            # If the flow direction is bottom right bottom, it should start from left or top
            if flow_direction[0] > 0 and flow_direction[0] > 0:
                if cls.random.random() > 0.5:
                    # start on top
                    position = (cls.random.randrange(0, cls.map_size[0]), 0)
                else:
                    # start on left
                    position = (0, cls.random.randrange(0, cls.map_size[1]))

            elif flow_direction[0] < 0 and flow_direction[0] < 0:
                if cls.random.random() > 0.5:
                    # start on right
                    position = (cls.map_size[0] - 1, cls.random.randrange(0, cls.map_size[1]))
                else:
                    # start on below
                    position = (cls.random.randrange(0, cls.map_size[1]), cls.map_size[1] - 1)

            elif flow_direction[0] > 0 and flow_direction[0] < 0:
                if cls.random.random() > 0.5:
                    # start on top
                    position = (0, cls.random.randrange(0, cls.map_size[1]))
                else:
                    # start on below
                    position = (cls.random.randrange(0, cls.map_size[1]), cls.map_size[1] - 1)

            elif flow_direction[0] < 0 and flow_direction[0] > 0:
                if cls.random.random() > 0.5:
                    # start on right
                    position = (cls.map_size[0] - 1, cls.random.randrange(0, cls.map_size[1]))
                else:
                    # start on top
                    position = (cls.random.randrange(0, cls.map_size[0]), 0)

            return position

        def next_position(position, flow_direction):
            import numpy as np

            # Get the next position according to the flow direction
            new_position = None
            direction = np.random.choice([0, 1], p=[flow_direction[0], flow_direction[1]])
            if direction == 0:
                new_position = (position[0] + int(flow_direction[0] / abs(flow_direction[0])), position[1])
            else:
                new_position = (position[0], position[1] + int(flow_direction[1] / abs(flow_direction[1])))

            return new_position

        # set flow direction
        left_right_flow = cls.random.random() * 2 - 1
        up_down_flow = cls.random.random() * 2 - 1
        flow_direction = (left_right_flow / ((left_right_flow ** 2 + up_down_flow ** 2) ** 0.5),
                          (up_down_flow / ((left_right_flow ** 2 + up_down_flow ** 2) ** 0.5)))

        # Sets the starting position of the valley bottom
        position = initial_position(flow_direction)
        cls.pits.append(position)

        # Generate valleys based on flow direction
        while cls.map_size[0] > position[0] >= 0 and cls.map_size[0] > position[1] >= 0:
            position = next_position(position, flow_direction)
            cls.pits_position.append(position)
            peak_value = cls.random.randrange(cls.pit_low_range[0], cls.pit_low_range[1])
            peak_surface_size = cls.random.randrange(2, 4)

            sub_value = 1
            # Slope up and down
            slope = cls.random.random()
            # When the effect is less than this value, the peak fails
            scope = 1
            cls.pits.append()


        cls.pits_position.append(position)
        cls.pits.append(Peak(position, sub_value, slope, scope))
        return cls.pits[-1]
