from world.exhibitor_super import Exhibitor_super


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


class Exhibitor(Exhibitor_super):
    """
        初始化在__init__和__init_exhibitor中
    """

    def __init__(self, world, block_size):
        self.world = world
        self.block_size = block_size
        # 地图长宽各多少格
        self.terrain_size = world.state.terrain_size
        # 窗口中世界的大小
        self.world_win_size = (self.block_size * self.terrain_size[0], self.block_size * self.terrain_size[1])
        # 窗口大小（加上状态栏）
        self.win_size = (self.world_win_size[1], self.world_win_size[0])
        self.__init_exhibitor()
        self.gate = True

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
                # 在第几行
                self.row = row
                # 在第几列
                self.col = col
                self.mid_interspace = interspace
                self.exhibitor = exhibitor
                # 屏幕宽度除以横向有几个格
                self.cell_width = exhibitor.world_win_size[1] / exhibitor.terrain_size[1]
                # 屏幕长度除以纵向有几个格
                self.cell_height = exhibitor.world_win_size[0] / exhibitor.terrain_size[0]
                # 求本格的位置
                self.left = self.col * self.cell_width
                self.top = self.row * self.cell_height

            def rect(self, color):
                pygame.draw.rect(self.exhibitor.window, color,
                                 (self.left, self.top, self.cell_width + 1, self.cell_height + 1))

            def mid_rect(self, color):
                pygame.draw.rect(self.exhibitor.window, color,
                                 (self.left + self.mid_interspace, self.top + self.mid_interspace,
                                  self.cell_width,
                                  self.cell_height))

            def box_rect(self, color):
                pygame.draw.rect(self.exhibitor.window, color,
                                 (self.left + self.mid_interspace, self.top + self.mid_interspace,
                                  self.cell_width + self.mid_interspace,
                                  self.cell_height + self.mid_interspace))

            def human_rect(self, color):
                pygame.draw.rect(self.exhibitor.window, color,
                                 (self.left + self.mid_interspace, self.top + self.mid_interspace,
                                  self.cell_width - self.mid_interspace,
                                  self.cell_height - self.mid_interspace))

            def mid_small_rect(self, color):
                pygame.draw.rect(self.exhibitor.window, color,
                                 (self.left + self.mid_interspace, self.top + self.mid_interspace,
                                  self.cell_width / 3,
                                  self.cell_height / 3))

            def small_circle(self, color):
                pygame.draw.circle(self.exhibitor.window, color,
                                   (self.left + self.cell_width / 3, self.top + self.cell_height / 3),
                                   self.cell_width / 3)

            def draw_plant_point(self, plant_species, color):
                self.exhibitor.pygame.draw.rect(self.exhibitor.window, color,
                                                (self.left + self.mid_interspace,
                                                 self.top + self.mid_interspace,
                                                 self.cell_height / 2,
                                                 self.cell_height * 9 / 10))

            def draw_bar(self, water_high, water_surface, max_water_high):
                water_surface.fill((0, 0, 255, max(0, min(water_high / (max_water_high + 5) * 200, 255))))
                self.exhibitor.window.blit(water_surface, (self.left, self.top))

        self.Point = Point

        # 定义颜色
        self.bg_color = (255, 255, 255)

    """
        展示的框架
    """

    def display(self, mode="ai"):
        """
        可视化的入口
            需要可视化的数据：
                地图
                    landform_map        [[int, int], [int, int], ...]            地势高低的地形地图                   每个数字代表该地方的高低值 可以为负数或任意正整数
                    water_map           [[float, float], [float, float], ...]    水地图 某个格的水位的高低             每个数字代表了该地方水位的高低 可以为任意小数值 不可以为负数
                    terrain_map         [[int, int], [int, int], ...]            地貌地图 描述某个地方的土是什么样的     由不同整数描述有土地 沙地 石地...等 数字从0到大 从干到湿 6为水底 5为沼泽 4为泥地 3为普通土地 2为沙地 1为鹅卵石地 0为大石地

                位置物体表
                    字典对象 存位置和位置上有的物体
                    animals_position    {(位置的横纵坐标): [<动物1>, <动物2>， ...], (a, b), [<>, ...], ...}
                    plants_position     {(位置的横纵坐标): [<植物1>, <植物2>， ...], (a, b), [<>, ...], ...}
                    objs_position       {(位置的横纵坐标): [<物品1>, <物品2>， ...], (a, b), [<>, ...], ...}

                玩家控制的生物（用于状态栏显示）（这个可以不弄）
                    player_controlling_unit
        """
        # 地图
        terrain = self.world.get_state().terrain

        # 位置物体表
        objs = self.world.get_state().objs

        # 玩家控制的生物
        player_controlling_unit = self.world.state.subjects[0]

        """
            画方格世界
        """
        self.draw_world(terrain, objs, player_controlling_unit)

        # 让渡控制权
        self.pygame.display.flip()

        # 设置帧率
        self.clock.tick(10)

        player_cmd = None
        # 读取玩家操作
        if mode == "normal":
            player_cmd = self.detect_player_input([])
        elif mode == "ai":
            player_cmd = None

        return player_cmd

    """
        画方格世界图
    """

    def draw_world(self, terrain, objs, player_controlling_unit):

        # 画地形和地貌
        def draw_landform_map(position, terrain):
            # 根据高度和地貌生成颜色
            def get_terrain_color(terrain_num, max_height, terrain):
                # 白 绿 棕 灰 黄 红 紫
                terrain_color = [(0.33333, 0.33333, 0.33333),
                                 (0.45, 0.1, 0.45),
                                 (0.8, 0.1, 0.1),
                                 (0.45, 0.45, 0.1),
                                 (0.33333, 0.33333, 0.33333),
                                 (0.396, 0.3396, 2642),
                                 (0.15, 0.7, 0.15),
                                 (0.33333, 0.33333, 0.33333)
                                 # (max_height / terrain_num, max_height / terrain_num, max_height / terrain_num)
                                 ]

                """
                    这里采用了我自己研究得出的亮度守恒公式
                    luminance = 0.3r + 0.6g + 0.1b
                """
                color_alpha = terrain_color[terrain][0] / max(terrain_color[terrain][1], 0.001)
                color_beta = terrain_color[terrain][1] / max(terrain_color[terrain][2], 0.001)
                color_gama = terrain_color[terrain][0] / max(terrain_color[terrain][2], 0.001)

                r_ratio = 1 / (0.3 + 0.6 * (1 / color_alpha) + 0.1 * (1 / color_gama))
                g_ratio = 1 / (0.3 * color_alpha + 0.6 + 0.1 * (1 / color_beta))
                b_ratio = 1 / (0.3 * color_gama + 0.6 * color_beta + 0.1)

                r = min(terrain_num / max_height * 225 * r_ratio, 255)
                g = min(terrain_num / max_height * 225 * g_ratio, 255)
                b = min(terrain_num / max_height * 225 * b_ratio, 255)
                return r, g, b

            self.Point\
                (self, row=position[0], col=position[1]).rect(get_terrain_color(100, 100, terrain))


        def draw_objs(objs):
            def get_obj_color(obj):
                import random
                # 强行将类名字符串转化为ord数字 作为种子
                random.seed(''.join(map(str, map(ord, type(obj).__name__))))
                r = random.randrange(0, 255)
                g = random.randrange(0, 255)
                b = random.randrange(0, 255)
                return r, g, b

            for obj in objs:
                position = obj.get_position()
                self.Point(self, row=position[0], col=position[1]).rect(get_obj_color(obj))

        """
            画图执行
        """

        # 渲染
        # 画方块
        # 画背景
        self.pygame.draw.rect(self.window, self.bg_color, (0, 0, self.win_size[0], self.win_size[1]))

        # 画地势
        for row_index in range(self.terrain_size[0]):
            for column_index in range(self.terrain_size[1]):
                draw_landform_map((row_index, column_index), terrain[row_index][column_index])

        # 画物品
        draw_objs(objs)

        position = player_controlling_unit.get_position()
        self.Point \
            (self, row=position[0], col=position[1]).rect((255, 0, 0))

    """
        检测玩家输入 玩家输入之前不会跳出循环 可能递归
    """

    def detect_player_input(self, last_code):

        # 等待按键 否则一直在循环里
        door = True
        while door and self.gate:
            # 处理事件
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    return False
                # keys = self.pygame.key.get_pressed()

                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_RIGHT:
                        last_code = "east"
                        door = False

                    elif event.key == self.pygame.K_DOWN:
                        last_code = "south"
                        door = False

                    elif event.key == self.pygame.K_LEFT:
                        last_code = "west"
                        door = False

                    elif event.key == self.pygame.K_UP:
                        last_code = "north"
                        door = False
        return last_code

    def set_out(self):
        self.gate = False
