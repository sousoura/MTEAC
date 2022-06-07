from world.exhibitor_super import Exhibitor_super
from world.world_project.mesh_world.PlayerViewWindow import PlayerView
import sys

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
        self.win_size = (self.world_win_size[1], self.world_win_size[0] + self.world_win_size[0] / 5)
        self.__init_exhibitor()

        self.gate = True

        self.playerControllingUnit = None

        self.directionPressed = [20, 20]
        self.cubeSize = 64  # 每个格的大小，素材全是64*64的

        self.player_id = 1

        """
            choose the version of visualization
        """
        self.version = 2

    # 初始化展示器
    def __init_exhibitor(self):
        # 初始化框架
        import pygame

        self.pygame = pygame

        # 初始化
        pygame.init()

        # 规定大小 生成窗口
        self.window = pygame.display.set_mode(self.win_size)
        self.PlayerView = PlayerView()

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

    def display(self, mode="normal"):
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
        landform_map = self.world.get_state().get_landform_map()
        water_map = self.world.get_state().get_water_map()
        terrain_map = self.world.get_state().get_terrain_map()

        # 位置物体表
        animals_position = self.world.get_state().get_animals_position()
        plants_position = self.world.get_state().get_plants_position()
        objs_position = self.world.get_state().get_objs_position()

        # 玩家控制的生物
        player_controlling_unit = self.world.get_state().get_entity_by_id(self.player_id)

        if player_controlling_unit:
            player_controlling_unit_position = list(player_controlling_unit.position)
        else:
            player_controlling_unit_position = [0, 0]

        # win_event = True

        """
            draw the world
        """
        if self.version == 1:
            self.draw_world(landform_map, water_map, terrain_map, animals_position, plants_position, objs_position)
        elif self.version == 2:
            self.player_view(terrain_map, animals_position, plants_position, objs_position, landform_map, self.win_size,
                             water_map, player_controlling_unit_position, mode)

        """
            画状态栏
        """
        self.draw_status_bar(player_controlling_unit)

        # 让渡控制权
        self.pygame.display.flip()

        # 设置帧率
        self.clock.tick(30)

        player_cmd = None
        # Read player actions by listening to the keyboard
        if mode == "normal":
            player_cmd = self.detect_player_input([])
        elif mode == "ai":
            player_cmd = None
        elif mode == "no_waiting":
            player_cmd = self.no_waiting_detect([])

            if player_cmd is False:
                return False
            elif len(player_cmd) == 0:
                player_cmd = ["rest"]

        return player_cmd

    """
        画方格世界图
    """

    def draw_world(self, landform_map, water_map, terrain_map, animals_position, plants_position, objs_position):
        # 找到全地图的最高点
        def get_maximum_height(landform_map):
            return max(map(max, landform_map))

        max_height = get_maximum_height(landform_map)
        max_water_high = get_maximum_height(water_map)

        """
            定义绘图函数
        """

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

            self.Point \
                (self, row=position[0], col=position[1]).rect(get_terrain_color(terrain_type, max_height, terrain))

        # 画水地图
        def draw_water_map(position, water_high):
            # 可视化半透明水层
            # water_surface = self.window.convert_alpha()
            water_surface = \
                self.pygame.Surface(
                    (self.world_win_size[0] / self.terrain_size[0] + 1,
                     self.world_win_size[1] / self.terrain_size[1] + 1)
                    , self.pygame.SRCALPHA, 32)
            self.Point(self, row=position[0], col=position[1]).draw_bar(water_high, water_surface, max_water_high)

        # 画生物
        # 画动物
        def draw_animals(position, animals):
            def get_animal_color(animal):
                import random
                # 强行将类名字符串转化为ord数字 作为种子
                random.seed(''.join(map(str, map(ord, type(animal).__name__))))
                r = random.randrange(0, 255)
                g = random.randrange(0, 255)
                b = random.randrange(0, 255)
                return r, g, b

            for animal in animals:
                self.Point(self, row=position[0], col=position[1]).mid_rect(get_animal_color(animal))

        # 画植物
        def draw_plants(position, plants):
            def get_plant_color(plant_species):
                return ((169, 208, 107), (205, 133, 63), (165, 42, 42), (0, 125, 0), (0, 255, 0))[plant_species]

            for plant in plants:
                plant_species = ["Algae", "Birch", "Birch_wood", "Grass", "Grassland"].index(type(plant).__name__)
                self.Point \
                    (self, row=position[0], col=position[1]). \
                    draw_plant_point(plant_species, get_plant_color(plant_species))

        def draw_objs(position, objs):
            def get_obj_color(obj):
                import random
                # 强行将类名字符串转化为ord数字 作为种子
                random.seed(''.join(map(str, map(ord, type(obj).__name__))))
                r = random.randrange(0, 255)
                g = random.randrange(0, 255)
                b = random.randrange(0, 255)
                return r, g, b

            for obj in objs:
                self.Point(self, row=position[0], col=position[1]).small_circle(get_obj_color(obj))

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
                draw_landform_map \
                    ((row_index, column_index), landform_map[row_index][column_index], max_height,
                     terrain_map[row_index][column_index])
                if water_map[row_index][column_index] > 0.5:
                    draw_water_map \
                        ((row_index, column_index), water_map[row_index][column_index])

        # 画物品
        for position in objs_position:
            draw_objs(position, objs_position[position])

        # 画生物
        # 画动物
        for position in animals_position:
            draw_animals(position, animals_position[position])

        # 画植物
        for position in plants_position:
            draw_plants(position, plants_position[position])

    def player_view(self, landFormMap, animals_position, plants_position, objs_position, HeightMap, win_size, water_map,
                    player_At, mode):

        # 画地图
        self.PlayerView.ReceiveVariable(landFormMap, animals_position, plants_position, objs_position, HeightMap,
                                        win_size, water_map)
        if mode != "ai":  # 玩家模式和AI模式中获取摄像机的逻辑有些许不同
            self.PlayerView.set_camera_topleft(player_At)
        else:
            # self.PlayerView.set_camera_topleft_Ai(self.directionPressed)
            self.PlayerView.set_camera_topleft(player_At)

        self.PlayerView.Update()

    """
        检测玩家输入 玩家输入之前不会跳出循环 可能递归
    """

    # Ai模式的输入为根据方向键移动摄像机
    def MoveCamera_input(self, landFormMap, win_size, cube_size):
        worldWidth = len(landFormMap[0])
        worldHeight = len(landFormMap)
        win_size[0] / cube_size / 2

        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.pygame.quit()
                sys.exit()
                return ["exit"]

            elif event.type == self.pygame.KEYDOWN:
                # 检测， 如果碰到边缘的话摄影机就不动
                if event.key == self.pygame.K_UP:
                    if 0 < self.directionPressed[0]:
                        self.directionPressed[0] -= 1

                elif event.key == self.pygame.K_DOWN:
                    if self.directionPressed[0] < worldHeight - int(win_size[1] / cube_size):
                        self.directionPressed[0] += 1

                elif event.key == self.pygame.K_LEFT:
                    if 0 < self.directionPressed[1]:
                        self.directionPressed[1] -= 1

                elif event.key == self.pygame.K_RIGHT:
                    if self.directionPressed[1] < worldWidth - int(win_size[0] / cube_size):
                        self.directionPressed[1] += 1

    def draw_status_bar(self, player_controlling_unit):

        """
            三个标题
        """

        # # 创建字体对象
        # title_font_size = 20
        # title_font = self.pygame.font.Font(None, title_font_size)
        #
        # # 文本与颜色
        # state_title_text = title_font.render("Creature state", True, (0, 0, 0))
        # attribute_title_text = title_font.render("Attribute state", True, (0, 0, 0))
        # species_characteristics_text = title_font.render("Species characteristics", True, (0, 0, 0))
        #
        # # 文本坐标
        # state_title_position = (self.world_win_size[0] / 9, self.world_win_size[1] * 102 / 100)
        # attribute_title_position = (self.world_win_size[0] / 8 * 2, self.world_win_size[1] * 102 / 100)
        # species_characteristics_position = (self.world_win_size[0] / 8 * 3, self.world_win_size[1] * 102 / 100)
        # # 获取设置后新的坐标区域
        # state_title_rect = state_title_text.get_rect(center=state_title_position)
        # attribute_title_rect = state_title_text.get_rect(center=attribute_title_position)
        # species_characteristics_rect = state_title_text.get_rect(center=species_characteristics_position)
        #
        # self.window.blit(state_title_text, state_title_rect)
        # self.window.blit(attribute_title_text, attribute_title_rect)
        # self.window.blit(species_characteristics_text, species_characteristics_rect)

        """
            属性
        """

        state_attribute = ["position", "life", "full_value", "drinking_value", "body_state", "backpack", "equipment"]
        ability_attribute = ["crawl_ability", "speed", "aggressivity"]
        ability_correct_attribute = ["crawl_ability_change_value", "speed_change_value", "aggressivity_change_value"]
        individual_attribute = ["gender"]
        action_mode_attribute = ["pace"]
        situation_attribute = ["situation"]
        species_characteristics_attribute = ["feeding_habits", "swimming_ability"]

        attribute_lists_list = [state_attribute, ability_attribute, ability_correct_attribute,
                                individual_attribute, action_mode_attribute, situation_attribute,
                                species_characteristics_attribute]

        if player_controlling_unit:
            row = 0
            col = 0
            init_position = (self.world_win_size[1] / 7, self.world_win_size[0] * 102 / 100)

            font_size = self.block_size
            text_font = self.pygame.font.Font(None, font_size)

            line_width = self.world_win_size[1] / 4
            line_high = font_size * 1.2

            # 遍历属性名
            for attribute_name in player_controlling_unit.__dir__():
                # 排除内置方法和属性
                if attribute_name[0] != "_":
                    # 排除方法对象
                    if not hasattr(getattr(player_controlling_unit, attribute_name), '__call__'):
                        for attribute_list in attribute_lists_list:
                            if attribute_name in attribute_list:
                                text_position = \
                                    (init_position[0] + row * line_width, init_position[1] + col * line_high)
                                attribute_value = getattr(player_controlling_unit, attribute_name)
                                if isinstance(attribute_value, (list, tuple)):
                                    elements_str = ""
                                    for element in attribute_value:
                                        elements_str += str(element) + ' '
                                    text = \
                                        text_font.render(attribute_name + ": " +
                                                         elements_str,
                                                         True, (0, 0, 0))
                                else:
                                    text = \
                                        text_font.render(attribute_name + ": " +
                                                         str(attribute_value),
                                                         True, (0, 0, 0))

                                text_rect = text.get_rect(center=text_position)
                                self.window.blit(text, text_rect)

                                col += 1
                                if col // 8 >= 1:
                                    col = 0
                                    row += 1

    """
        检测玩家输入 玩家输入之前不会跳出循环 可能递归
    """

    def detect_player_input(self, last_code):
        if len(self.world.get_state().get_animals()) > 0:
            player_animal = self.world.get_state().get_entity_by_id(self.player_id)
        else:
            print("动物死光光")
            return False
        # 作用于方向和对象的动作的名称的数组
        direction_and_obj_action = ["eat", "attack", "pick_up", "put_down", "push"]
        direction_and_objs_action = ["construct"]
        direction_action = ["drink", "collect"]
        backpack_action = ["put_down", "fabricate"]

        # 等待输入数字参数
        def waiting_for_para(last_code):
            # 等待按键 否则一直在循环里
            while True and self.gate:
                # 处理事件
                for event_para_wait in self.pygame.event.get():
                    if event.type == self.pygame.QUIT:
                        return False

                    if event_para_wait.type == self.pygame.KEYDOWN:
                        if event_para_wait.key == self.pygame.K_1:
                            last_code.append(1)
                            return True
                        elif event_para_wait.key == self.pygame.K_2:
                            last_code.append(2)
                            return True
                        elif event_para_wait.key == self.pygame.K_3:
                            last_code.append(3)
                            return True
                        elif event_para_wait.key == self.pygame.K_4:
                            last_code.append(4)
                            return True
                        elif event_para_wait.key == self.pygame.K_5:
                            last_code.append(5)
                            return True
                        elif event_para_wait.key == self.pygame.K_6:
                            last_code.append(6)
                            return True
                        elif event_para_wait.key == self.pygame.K_7:
                            last_code.append(7)
                            return True
                        elif event_para_wait.key == self.pygame.K_8:
                            last_code.append(8)
                            return True
                        elif event_para_wait.key == self.pygame.K_DELETE:
                            last_code.append(-1)
                            return True
                        elif event_para_wait.key == self.pygame.K_RETURN:
                            last_code.append("OK")
                            return True

        # 请求选择作用对象
        """
            从世界取得该位置的实例
            然后玩家输入下标选择对象是那个
        """

        def choose_object(last_code):
            if player_animal.get_id() == 1:
                objects_num = 0
                if last_code[0] in backpack_action:
                    if type(player_animal).__name__ == "Human_being":
                        entities = player_animal.get_backpack()
                        objects_num = len(entities)
                    else:
                        print("警告 发现非人类调用人类背包动作 程序存在bug")
                        return False
                elif last_code[0] in direction_and_obj_action:
                    old_position = tuple(player_animal.get_position())
                    position = self.world.get_state().position_and_direction_get_adjacent(old_position, last_code[1])
                    entities = self.world.get_state().get_entities_in_position(position)
                    objects_num = len(entities)
                # 如果只有一个可选对象 且符合条件 则马上返回之
                if objects_num == 1:
                    last_code.append(entities[0])
                    return True
                # 若压根无对象 则返回-1
                if objects_num == 0:
                    last_code.append(-1)
                    return True

                """
                    目前只能通过终端给玩家呈现对象们以选择
                    到时候可以直接在下面的呈现栏里给玩家呈现
                """
                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()
                    if 0 < input_num <= objects_num:
                        be_eator = entities[input_num - 1]
                        last_code.append(be_eator)
                        return True
                    # 反悔操作
                    elif input_num == -1:
                        last_code.append(-1)
                        return True
                    else:
                        last_code.append(-1)
                        return True

                else:
                    return False
            else:
                print("Waining: the id of the entity player controlling is not 1.")
                last_code.append(-1)
                return True

        def choose_object_from_backpack():
            if player_animal.get_id() == 1:
                if type(player_animal).__name__ == "Human_being":
                    entities = player_animal.get_backpack()[:]
                else:
                    print("警告 发现非人类调用人类背包动作 程序存在bug")
                    return -1

                """
                    目前只能通过终端给玩家呈现对象们以选择
                    到时候可以直接在下面的呈现栏里给玩家呈现
                """
                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()

                    if input_num == "OK":
                        return None
                    elif 0 <= input_num - 1 < len(entities):
                        be_selector = entities.pop(input_num - 1)
                        return be_selector
                    # 反悔操作
                    elif input_num == -1:
                        return -1
                    else:
                        return -1

                else:
                    return -2
            else:
                print("Waining: the id of the entity player controlling is not 1.")
                return -1

        def multi_choose_object_from_backpack():
            objs_list = []
            if player_animal.get_id() == 1:
                if type(player_animal).__name__ == "Human_being":
                    entities = player_animal.get_backpack()[:]
                    objects_num = len(entities)
                else:
                    print("警告 发现非人类调用人类背包动作 程序存在bug")
                    return -1
                # 如果只有一个可选对象 且符合条件 则马上返回之
                if objects_num == 1:
                    objs_list.append([entities[0]])
                    return objs_list
                # 若压根无对象 则返回-1
                if objects_num == 0:
                    return -1

                """
                    目前只能通过终端给玩家呈现对象们以选择
                    到时候可以直接在下面的呈现栏里给玩家呈现
                """
                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()

                    if input_num == "OK":
                        return objs_list
                    elif 0 <= input_num - 1 < len(entities):
                        be_selector = entities.pop(input_num - 1)
                        objs_list.append(be_selector)
                        print("now selected: ")
                        print_list_with_num(objs_list)
                        print_list_with_num(entities)
                    # 反悔操作
                    elif input_num == -1:
                        return -1
                    else:
                        return -1

                else:
                    return -2
            else:
                print("Waining: the id of the entity player controlling is not 1.")
                return -1

        # 建造用的 原材料选择
        def choose_objs_from_backpack_and_position(last_code):
            material_list = []
            if type(player_animal).__name__ == "Human_being":
                # 取得可选项目 从人类背包和该位置
                old_position = tuple(player_animal.get_position())
                position = self.world.get_state().position_and_direction_get_adjacent(old_position, last_code[1])
                entities = \
                    player_animal.get_backpack()[:] + self.world.get_state().get_entities_in_position(position)[:]
                objects_num = len(entities)

                # 如果只有一个可选对象 且符合条件 则马上返回之
                if objects_num == 1:
                    material_list.append(entities[0])
                    last_code.append(material_list)
                    return True

                # 若压根无对象 则返回-1
                if objects_num == 0:
                    last_code.append(-1)
                    return True

                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()

                    if input_num == "OK":
                        last_code.append(material_list)
                        return True
                    elif 0 <= input_num - 1 < len(entities):
                        be_selector = entities.pop(input_num - 1)
                        material_list.append(be_selector)

                        print("now selected: ")
                        print_list_with_num(material_list)
                        print_list_with_num(entities)

                    # 反悔操作
                    elif input_num == -1:
                        last_code.append(-1)
                        return True
                    else:
                        last_code.append(-1)
                        return True

            else:
                print("警告 发现非人类调用人类背包动作 程序存在bug")
                last_code.append(-1)
                return True
            last_code.append(material_list)

        def print_list_with_num(lis):
            num = 1
            print()
            for entity in lis:
                print(str(num) + ': ' + type(entity).__name__, "ID:", entity.get_id())
                num += 1
            print()

        """
            吃 z       攻击 x     喝 c      休息 v
            合成 f      建造 r     
            拾起 a      放下 s      装备 e    收集 g   
            推拉 t
        """

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
                    if event.key == self.pygame.K_UP:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("up")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("up")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("up")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("up")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_DOWN:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("down")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("down")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("down")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("down")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_LEFT:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("left")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("left")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("left")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("left")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_RIGHT:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("right")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("right")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("right")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("right")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_z:
                        last_code.append("eat")
                        self.detect_player_input(last_code)
                        door = False

                    elif event.key == self.pygame.K_x:
                        last_code.append("attack")
                        self.detect_player_input(last_code)
                        door = False

                    elif event.key == self.pygame.K_c:
                        last_code.append("drink")
                        self.detect_player_input(last_code)
                        door = False

                    elif event.key == self.pygame.K_v:
                        if len(last_code) == 0:
                            last_code.append("rest")
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("stay")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("stay")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("stay")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_a:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("pick_up")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_s:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("put_down")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_e:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("handling")
                                last_code.append("")
                                last_code.append(choose_object_from_backpack())
                                door = False

                    elif event.key == self.pygame.K_f:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("fabricate")
                                last_code.append("")
                                last_code.append(multi_choose_object_from_backpack())
                                # 若关闭程序
                                if last_code[-1] == -2:
                                    self.pygame.quit()
                                    return False
                                door = False

                    elif event.key == self.pygame.K_r:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("construct")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_g:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("collect")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_t:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("push")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_1:
                        player_animal.change_pace(1)
                    elif event.key == self.pygame.K_2:
                        player_animal.change_pace(2)
                    elif event.key == self.pygame.K_3:
                        player_animal.change_pace(3)
                    elif event.key == self.pygame.K_4:
                        player_animal.change_pace(4)
                    elif event.key == self.pygame.K_5:
                        player_animal.change_pace(5)
                    elif event.key == self.pygame.K_6:
                        player_animal.change_pace(6)
                    elif event.key == self.pygame.K_7:
                        player_animal.change_pace(7)
                    elif event.key == self.pygame.K_8:
                        player_animal.change_pace(8)

        return last_code

    def no_waiting_detect(self, last_code):
        if len(self.world.get_state().get_animals()) > 0:
            player_animal = self.world.get_state().get_entity_by_id(self.player_id)
        else:
            print("动物死光光")
            return False
        # 作用于方向和对象的动作的名称的数组
        direction_and_obj_action = ["eat", "attack", "pick_up", "put_down", "push"]
        direction_and_objs_action = ["construct"]
        direction_action = ["drink", "collect"]
        backpack_action = ["put_down", "fabricate"]

        # 等待输入数字参数
        def waiting_for_para(last_code):
            # 等待按键 否则一直在循环里
            while True and self.gate:
                # 处理事件
                for event_para_wait in self.pygame.event.get():
                    if event.type == self.pygame.QUIT:
                        return False

                    if event_para_wait.type == self.pygame.KEYDOWN:
                        if event_para_wait.key == self.pygame.K_1:
                            last_code.append(1)
                            return True
                        elif event_para_wait.key == self.pygame.K_2:
                            last_code.append(2)
                            return True
                        elif event_para_wait.key == self.pygame.K_3:
                            last_code.append(3)
                            return True
                        elif event_para_wait.key == self.pygame.K_4:
                            last_code.append(4)
                            return True
                        elif event_para_wait.key == self.pygame.K_5:
                            last_code.append(5)
                            return True
                        elif event_para_wait.key == self.pygame.K_6:
                            last_code.append(6)
                            return True
                        elif event_para_wait.key == self.pygame.K_7:
                            last_code.append(7)
                            return True
                        elif event_para_wait.key == self.pygame.K_8:
                            last_code.append(8)
                            return True
                        elif event_para_wait.key == self.pygame.K_DELETE:
                            last_code.append(-1)
                            return True
                        elif event_para_wait.key == self.pygame.K_RETURN:
                            last_code.append("OK")
                            return True

        # 请求选择作用对象
        """
            从世界取得该位置的实例
            然后玩家输入下标选择对象是那个
        """

        def choose_object(last_code):
            if player_animal.get_id() == 1:
                objects_num = 0
                if last_code[0] in backpack_action:
                    if type(player_animal).__name__ == "Human_being":
                        entities = player_animal.get_backpack()
                        objects_num = len(entities)
                    else:
                        print("警告 发现非人类调用人类背包动作 程序存在bug")
                        return False
                elif last_code[0] in direction_and_obj_action:
                    old_position = tuple(player_animal.get_position())
                    position = self.world.get_state().position_and_direction_get_adjacent(old_position, last_code[1])
                    entities = self.world.get_state().get_entities_in_position(position)
                    objects_num = len(entities)
                # 如果只有一个可选对象 且符合条件 则马上返回之
                if objects_num == 1:
                    last_code.append(entities[0])
                    return True
                # 若压根无对象 则返回-1
                if objects_num == 0:
                    last_code.append(-1)
                    return True

                """
                    目前只能通过终端给玩家呈现对象们以选择
                    到时候可以直接在下面的呈现栏里给玩家呈现
                """
                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()
                    if 0 < input_num <= objects_num:
                        be_eator = entities[input_num - 1]
                        last_code.append(be_eator)
                        return True
                    # 反悔操作
                    elif input_num == -1:
                        last_code.append(-1)
                        return True
                    else:
                        last_code.append(-1)
                        return True

                else:
                    return False
            else:
                print("Waining: the id of the entity player controlling is not 1.")
                last_code.append(-1)
                return True

        def choose_object_from_backpack():
            if player_animal.get_id() == 1:
                if type(player_animal).__name__ == "Human_being":
                    entities = player_animal.get_backpack()[:]
                else:
                    print("警告 发现非人类调用人类背包动作 程序存在bug")
                    return -1

                """
                    目前只能通过终端给玩家呈现对象们以选择
                    到时候可以直接在下面的呈现栏里给玩家呈现
                """
                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()

                    if input_num == "OK":
                        return None
                    elif 0 <= input_num - 1 < len(entities):
                        be_selector = entities.pop(input_num - 1)
                        return be_selector
                    # 反悔操作
                    elif input_num == -1:
                        return -1
                    else:
                        return -1

                else:
                    return -2
            else:
                print("Waining: the id of the entity player controlling is not 1.")
                return -1

        def multi_choose_object_from_backpack():
            objs_list = []
            if player_animal.get_id() == 1:
                if type(player_animal).__name__ == "Human_being":
                    entities = player_animal.get_backpack()[:]
                    objects_num = len(entities)
                else:
                    print("警告 发现非人类调用人类背包动作 程序存在bug")
                    return -1
                # 如果只有一个可选对象 且符合条件 则马上返回之
                if objects_num == 1:
                    objs_list.append([entities[0]])
                    return objs_list
                # 若压根无对象 则返回-1
                if objects_num == 0:
                    return -1

                """
                    目前只能通过终端给玩家呈现对象们以选择
                    到时候可以直接在下面的呈现栏里给玩家呈现
                """
                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()

                    if input_num == "OK":
                        return objs_list
                    elif 0 <= input_num - 1 < len(entities):
                        be_selector = entities.pop(input_num - 1)
                        objs_list.append(be_selector)
                        print("now selected: ")
                        print_list_with_num(objs_list)
                        print_list_with_num(entities)
                    # 反悔操作
                    elif input_num == -1:
                        return -1
                    else:
                        return -1

                else:
                    return -2
            else:
                print("Waining: the id of the entity player controlling is not 1.")
                return -1

        # 建造用的 原材料选择
        def choose_objs_from_backpack_and_position(last_code):
            material_list = []
            if type(player_animal).__name__ == "Human_being":
                # 取得可选项目 从人类背包和该位置
                old_position = tuple(player_animal.get_position())
                position = self.world.get_state().position_and_direction_get_adjacent(old_position, last_code[1])
                entities = \
                    player_animal.get_backpack()[:] + self.world.get_state().get_entities_in_position(position)[:]
                objects_num = len(entities)

                # 如果只有一个可选对象 且符合条件 则马上返回之
                if objects_num == 1:
                    material_list.append(entities[0])
                    last_code.append(material_list)
                    return True

                # 若压根无对象 则返回-1
                if objects_num == 0:
                    last_code.append(-1)
                    return True

                print_list_with_num(entities)

                # 判断对象选择是否合法
                temp_list = []
                while waiting_for_para(temp_list):
                    input_num = temp_list.pop()

                    if input_num == "OK":
                        last_code.append(material_list)
                        return True
                    elif 0 <= input_num - 1 < len(entities):
                        be_selector = entities.pop(input_num - 1)
                        material_list.append(be_selector)

                        print("now selected: ")
                        print_list_with_num(material_list)
                        print_list_with_num(entities)

                    # 反悔操作
                    elif input_num == -1:
                        last_code.append(-1)
                        return True
                    else:
                        last_code.append(-1)
                        return True

            else:
                print("警告 发现非人类调用人类背包动作 程序存在bug")
                last_code.append(-1)
                return True
            last_code.append(material_list)

        def print_list_with_num(lis):
            num = 1
            print()
            for entity in lis:
                print(str(num) + ': ' + type(entity).__name__, "ID:", entity.get_id())
                num += 1
            print()

        """
            吃 z       攻击 x     喝 c      休息 v
            合成 f      建造 r     
            拾起 a      放下 s      装备 e    收集 g   
            推拉 t
        """

        # 等待按键 否则一直在循环里
        door = True
        if door and self.gate:
            # 处理事件
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    return False
                # keys = self.pygame.key.get_pressed()

                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_UP:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("up")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("up")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("up")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("up")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_DOWN:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("down")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("down")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("down")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("down")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_LEFT:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("left")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("left")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("left")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("left")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_RIGHT:
                        if len(last_code) == 0:
                            last_code.append("go")
                            last_code.append("right")
                            # if not waiting_for_para(last_code):
                            #     return False
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("right")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("right")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("right")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_z:
                        last_code.append("eat")
                        self.detect_player_input(last_code)
                        door = False

                    elif event.key == self.pygame.K_x:
                        last_code.append("attack")
                        self.detect_player_input(last_code)
                        door = False

                    elif event.key == self.pygame.K_c:
                        last_code.append("drink")
                        self.detect_player_input(last_code)
                        door = False

                    elif event.key == self.pygame.K_v:
                        if len(last_code) == 0:
                            last_code.append("rest")
                        elif last_code[0] in direction_and_obj_action:
                            last_code.append("stay")
                            if not choose_object(last_code):
                                self.pygame.quit()
                                return False
                        elif last_code[0] in direction_action:
                            last_code.append("stay")
                        elif last_code[0] in direction_and_objs_action:
                            last_code.append("stay")
                            choose_objs_from_backpack_and_position(last_code)
                        door = False

                    elif event.key == self.pygame.K_a:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("pick_up")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_s:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("put_down")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_e:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("handling")
                                last_code.append("")
                                last_code.append(choose_object_from_backpack())
                                door = False

                    elif event.key == self.pygame.K_f:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("fabricate")
                                last_code.append("")
                                last_code.append(multi_choose_object_from_backpack())
                                # 若关闭程序
                                if last_code[-1] == -2:
                                    self.pygame.quit()
                                    return False
                                door = False

                    elif event.key == self.pygame.K_r:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("construct")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_g:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("collect")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_t:
                        if type(player_animal).__name__ == "Human_being":
                            if len(last_code) == 0:
                                last_code.append("push")
                                self.detect_player_input(last_code)
                                door = False

                    elif event.key == self.pygame.K_1:
                        player_animal.change_pace(1)
                    elif event.key == self.pygame.K_2:
                        player_animal.change_pace(2)
                    elif event.key == self.pygame.K_3:
                        player_animal.change_pace(3)
                    elif event.key == self.pygame.K_4:
                        player_animal.change_pace(4)
                    elif event.key == self.pygame.K_5:
                        player_animal.change_pace(5)
                    elif event.key == self.pygame.K_6:
                        player_animal.change_pace(6)
                    elif event.key == self.pygame.K_7:
                        player_animal.change_pace(7)
                    elif event.key == self.pygame.K_8:
                        player_animal.change_pace(8)

        return last_code

    def set_out(self):
        self.gate = False
