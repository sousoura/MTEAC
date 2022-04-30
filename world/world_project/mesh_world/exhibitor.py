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
            row = 0
            col = 0

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
                                  self.cell_width - 2 * self.mid_interspace, self.cell_height - 2 * self.mid_interspace))

        self.Point = Point

        # 定义颜色
        self.bg_color = (255, 255, 255)

    """
        展示的框架
    """
    def display(self, world):
        terrain = world.get_state().get_terrain()
        things_position = world.get_state().get_things_position()
        # win_event = True

        self.draw(terrain, things_position)

        # 让渡控制权
        self.pygame.display.flip()

        # 设置帧率
        self.clock.tick(60)

        return self.detect_player_input("")

    """
        画图
    """
    def draw(self, terrain, things_position):
        def draw_terrain(position, terrain_type):
            # 根据一个数字得到一个随机颜色 确保同一数字得到的总是同一颜色
            def get_terrain_color(terrain_num):
                import random
                random.seed(terrain_num)
                r = random.randrange(0, 255)
                g = random.randrange(0, 255)
                b = random.randrange(0, 255)
                return r, g, b

            self.Point(self, row=position[1], col=position[0]).rect(get_terrain_color(terrain_type))

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

        # 画地形
        for block_line_index in range(len(terrain)):
            for block_index in range(len(terrain[block_line_index])):
                draw_terrain((block_index, block_line_index), terrain[block_line_index][block_index])

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
