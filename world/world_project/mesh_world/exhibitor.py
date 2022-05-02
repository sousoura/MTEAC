"""
    展示器类
    职能：窗口化和可视化都在这个类里头
    属性：
        地图大小
        窗口大小
        pygame
        window对象
        Point类
        bg_color
    方法：
        两个用于初始化的方法
            __init__
            __init_exhibitor
        display用于真正输出
            本体为框架
            真正需要编辑的在draw()里面
                两个分别画地形和生物的工具方法 在draw中使用
            其中detect_player_input用于渲染完毕后读取用户输入
"""


class Exhibitor:
    """
        初始化在__init__和__init_exhibitor中
    """

    def __init__(self, world, win_size):
        self.terrain_size = world.state.terrain_size
        self.win_size = win_size
        self.__init_exhibitor()

    # 初始化展示器
    def __init_exhibitor(self):
        # 初始化框架
        import pygame

        self.pygame = pygame

        # 初始化
        pygame.init()

        # 规定大小 生成窗口
        self.window = pygame.display.set_mode(self.win_size)

        # 设置标题
        pygame.display.set_caption("MTEAC")

        # 设定时间频率
        self.clock = pygame.time.Clock()

        # 定义点类
        class Point:
            def __init__(self, exhibitor, row, col, interspace=5):
                self.row = row
                self.col = col
                self.mid_interspace = interspace
                self.exhibitor = exhibitor
                self.cell_width = exhibitor.win_size[0] / exhibitor.terrain_size[0]
                self.cell_height = exhibitor.win_size[1] / exhibitor.terrain_size[1]
                self.left = self.col * self.cell_width
                self.top = self.row * self.cell_height

            def rect(self, color):
                pygame.draw.rect(self.exhibitor.window, color, (self.left, self.top, self.cell_width, self.cell_height))

            def mid_rect(self, color):
                pygame.draw.rect(self.exhibitor.window, color,
                                 (self.left + self.mid_interspace, self.top + self.mid_interspace,
                                  self.cell_width - 2 * self.mid_interspace,
                                  self.cell_height - 2 * self.mid_interspace))

        self.Point = Point

        # 定义颜色
        self.bg_color = (255, 255, 255)

    """
        展示的框架
    """

    def display(self, world):

        landform_map = world.get_state().get_landform_map()
        water_map = world.get_state().get_water_map()
        terrain_map = world.get_state().get_terrain_map()
        things_position = world.get_state().get_things_position()

        # win_event = True

        self.draw(landform_map, water_map, terrain_map, things_position)

        # 让渡控制权
        self.pygame.display.flip()

        # 设置帧率
        self.clock.tick(60)

        return self.detect_player_input("")

    """
        画图
    """

    def draw(self, landform_map, water_map, terrain_map, things_position):
        # 找到全地图的最高点
        def get_maximum_height(landform_map):
            return max(map(max, landform_map))

        max_height = get_maximum_height(landform_map)
        max_water_high = get_maximum_height(water_map)

        # 画地形和地貌
        def draw_landform_map(position, terrain_type, max_height, terrain):
            # 根据高度和地貌生成颜色
            def get_terrain_color(terrain_num, max_height, terrain):
                # 白 绿 棕 灰 黄 红 紫
                terrain_color = [(0.45, 0.1, 0.45),
                                 (0.8, 0.1, 0.1),
                                 (0.45, 0.45, 0.1),
                                 (0.33333, 0.33333, 0.33333),
                                 (0.396, 0.3396, 2642),
                                 (0.15, 0.7, 0.15),
                                 (0.33333, 0.33333, 0.33333)
                                 # (max_height / terrain_num, max_height / terrain_num, max_height / terrain_num)
                                 ]

                r = min(terrain_num / max_height * 225 * terrain_color[terrain][0], 255)
                g = min(terrain_num / max_height * 225 * terrain_color[terrain][1], 255)
                b = min(terrain_num / max_height * 225 * terrain_color[terrain][2], 255)
                return r, g, b

            self.Point\
                (self, row=position[1], col=position[0]).rect(get_terrain_color(terrain_type, max_height, terrain))

        # 画水地图
        class Water_point(self.Point):
            color = (0, 0, 225)

            def __init__(self, exhibitor, row, col, water_surface, interspace=5):
                super(Water_point, self).__init__(exhibitor, row, col, interspace)
                self.water_surface = water_surface

            @classmethod
            def set_max_water_high(cls, max_water_high):
                cls.max_water_high = max_water_high

            def draw_bar(self, water_high, water_surface):
                water_surface.fill((0, 0, 255, min(water_high / (self.max_water_high + 5) * 200, 255)))
                # self.exhibitor.window.draw.rect(
                #     self.water_surface,
                #     self.exhibitor.pygame.Color(0, 0, 255, int(min(water_high * 10 / max_water_high * 225))),
                #     # (self.color[0],
                #     #  self.color[1],
                #     #  self.color[2],
                #     #  min(water_high * 10 / max_water_high * 225, 225)
                #     #  ),
                #      (self.left, self.top, self.cell_width, self.cell_height)
                #      )
                self.exhibitor.window.blit(water_surface, (self.left, self.top))

        def draw_water_map(position, water_high):
            # 可视化半透明水层
            # water_surface = self.window.convert_alpha()
            water_surface = \
                self.pygame.Surface(
                    (self.win_size[0] / self.terrain_size[0],
                     self.win_size[1] / self.terrain_size[1])
                    , self.pygame.SRCALPHA, 32)
            Water_point(self, row=position[1], col=position[0], water_surface=water_surface).\
                draw_bar(water_high, water_surface)

        # 画生物
        def draw_creatures(position, creatures):
            def get_creature_color(creature):
                import random
                # 强行将类名字符串转化为ord数字 作为种子
                random.seed(''.join(map(str, map(ord, type(creature).__name__))))
                r = random.randrange(0, 255)
                g = random.randrange(0, 255)
                b = random.randrange(0, 255)
                return r, g, b

            for creature in creatures:
                self.Point(self, row=position[1], col=position[0]).mid_rect(get_creature_color(creature))

        # 渲染
        # 画方块
        # 画背景
        self.pygame.draw.rect(self.window, self.bg_color, (0, 0, self.win_size[0], self.win_size[1]))
        Water_point.set_max_water_high(max_water_high)

        # 画地形
        for block_line_index in range(len(landform_map)):
            for block_index in range(len(landform_map[block_line_index])):
                draw_landform_map \
                    ((block_index, block_line_index), landform_map[block_line_index][block_index], max_height,
                     terrain_map[block_line_index][block_index])
                if water_map[block_line_index][block_index] > 0.5:
                    draw_water_map \
                        ((block_index, block_line_index), water_map[block_line_index][block_index])

        # 画生物
        for position in things_position:
            draw_creatures(position, things_position[position])

    """
        检测玩家输入 玩家输入之前不会跳出循环 可能递归
    """

    def detect_player_input(self, last_code):
        # 等待按键 否则一直在循环里
        door = True
        while door:
            # 处理事件
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    return False
                # keys = self.pygame.key.get_pressed()

                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_UP:
                        last_code += "up"
                        door = False
                    elif event.key == self.pygame.K_DOWN:
                        last_code += "down"
                        door = False
                    elif event.key == self.pygame.K_LEFT:
                        last_code += "left"
                        door = False
                    elif event.key == self.pygame.K_RIGHT:
                        last_code += "right"
                        door = False
                    elif event.key == self.pygame.K_SPACE:
                        last_code += "eat_"
                        last_code = self.detect_player_input(last_code)
                        door = False

        return last_code
