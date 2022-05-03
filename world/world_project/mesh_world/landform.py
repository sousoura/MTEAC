from abc import ABCMeta, abstractmethod


"""
    使用 山峰Peak 山脉Ridge 坑地Pit 谷地Valley的方法定义高低地形
    eve在这里码代码
    山峰已经完成了 现在打算做另外三个
        注意所有地形类型都继承Landform
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
        cls.random_seed = random_seed

    @abstractmethod
    def affect(self, point_position):
        pass


class Peak(Landform):
    peaks = []
    peaks_position = []
    peak_high_range = (2, 6)
    import random
    random = random
    random_seed = 114514
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
        # 上下左右的坡度
        slope = cls.random.random() * 0.05
        # slope = cls.random.random() * 0.7
        # 当影响小于这一值时 峰值失效
        scope = 1

        cls.peaks_position.append(position)
        cls.peaks.append(Peak(position, peak_value, peak_surface_size, slope, scope))
        return cls.peaks[-1]

    def affect(self, point_position):
        # 计算改点离山顶的距离
        distance = (point_position[0] - self.position[0]) ** 2 + (point_position[1] - self.position[1]) ** 2
        # 计算山对改点的高度的影响
        # 山顶的高度 减去距离乘以陡峭度
        affect = self.degree_value - distance * self.slope
        # 如果影响为负 或太小 则取消该影响
        # self.degree_value = 6
        if affect < self.scope:
            affect = 0
        # 返回影响的值
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
        通过定义初始点和流向的方法定义一个沟渠
            流向是一个单位向量 代表往下个方向生成的概率的权重
            如果流向是向右下方的 就不会想左或上方走
    """
    @classmethod
    def init_new_landform(cls):
        class Pit_point():
            pass

        def initial_position(flow_direction):
            position = (cls.map_size[0] - 1, cls.map_size[1] - 1)
            # 如果流向是右下 谷底则应该从左边或者上面开始
            if flow_direction[0] > 0 and flow_direction[0] > 0:
                if cls.random.random() > 0.5:
                    # 在上面开始
                    position = (cls.random.randrange(0, cls.map_size[0]), 0)
                else:
                    # 在左面开始
                    position = (0, cls.random.randrange(0, cls.map_size[1]))

            elif flow_direction[0] < 0 and flow_direction[0] < 0:
                if cls.random.random() > 0.5:
                    # 在右边开始
                    position = (cls.map_size[0] - 1, cls.random.randrange(0, cls.map_size[1]))
                else:
                    # 在下边开始
                    position = (cls.random.randrange(0, cls.map_size[1]), cls.map_size[1] - 1)

            elif flow_direction[0] > 0 and flow_direction[0] < 0:
                if cls.random.random() > 0.5:
                    # 在左面开始
                    position = (0, cls.random.randrange(0, cls.map_size[1]))
                else:
                    # 在下边开始
                    position = (cls.random.randrange(0, cls.map_size[1]), cls.map_size[1] - 1)

            elif flow_direction[0] < 0 and flow_direction[0] > 0:
                if cls.random.random() > 0.5:
                    # 在右边开始
                    position = (cls.map_size[0] - 1, cls.random.randrange(0, cls.map_size[1]))
                else:
                    # 在上面开始
                    position = (cls.random.randrange(0, cls.map_size[0]), 0)

            return position

        def next_position(position, flow_direction):
            import numpy as np

            # 依照流向得到下一个位置
            new_position = None
            direction = np.random.choice([0, 1], p=[flow_direction[0], flow_direction[1]])
            if direction == 0:
                new_position = (position[0] + int(flow_direction[0] / abs(flow_direction[0])), position[1])
            else:
                new_position = (position[0], position[1] + int(flow_direction[1] / abs(flow_direction[1])))

            return new_position

        # 设置流向
        left_right_flow = cls.random.random() * 2 - 1
        up_down_flow = cls.random.random() * 2 - 1
        flow_direction = (left_right_flow / ((left_right_flow ** 2 + up_down_flow ** 2) ** 0.5),
                          (up_down_flow / ((left_right_flow ** 2 + up_down_flow ** 2) ** 0.5)))

        # 设置山谷的谷底的起始位置
        position = initial_position(flow_direction)
        cls.pits.append(position)

        # 根据流向生成谷
        while cls.map_size[0] > position[0] >= 0 and cls.map_size[0] > position[1] >= 0:
            position = next_position(position, flow_direction)
            cls.pits_position.append(position)
            peak_value = cls.random.randrange(cls.pit_low_range[0], cls.pit_low_range[1])
            peak_surface_size = cls.random.randrange(2, 4)

            sub_value = 1
            # 上下左右的坡度
            slope = cls.random.random()
            # 当影响小于这一值时 峰值失效
            scope = 1
            cls.pits.append()


        cls.pits_position.append(position)
        cls.pits.append(Peak(position, sub_value, slope, scope))
        return cls.pits[-1]
