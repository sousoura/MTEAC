import importlib
import threading
from world.file_processor import File_processor

import gym
import random
import numpy as np
from gym import Env, spaces

"""
    代表MTEAC程序的类
    负责的功能：
        程序的入口
        整个程序的不断运行
        输入输出：窗口化显示 后台
"""


# 控制整个程序的进程
class WorldEnv(Env):
    """
        程序入口 让用户做初始化选择
        让程序不断运作下去
        分为两个线程
            程序和窗口线程
            后台命令线程
    """

    def __init__(self):
        # self.world_type_name = input("Please input world type name: ")
        # self.world_type_name = "mesh_world"
        # self.world_type_name = "eight_direction_mesh_world"
        self.world_type_name = "hexagonal_mesh_world"

        self.generator = None

        # 整个程序的起点
        # 生成世界
        """
            用户选择进入哪个世界 生成还是读取
        """
        print("开始创建世界")
        self.world = self.world_create()
        print("世界创建结束")

        if self.world:
            """
                Exhibitor负责窗口的可视化呈现
                每个世界方案都必须有一个Exhibitor类 哪怕为空
            """
            # 创建可视化窗口 后面那个数是世界的格子大小
            print("开始创建可视化")
            exhibitor_file = 'world.world_project.' + self.world_type_name + '.' + 'exhibitor'
            exhibitor_module = importlib.import_module(exhibitor_file)
            """
                参数是每个格的大小
            """
            self.exhibitor = exhibitor_module.Exhibitor(self.world, 15)
            print("可视化创建结束")

        self.seed()

        self.action_space, self.observation_space = self.world.get_openai_action_space_and_observation_space()

    # 程序入口
    """
        负责用户的初始化选择
        用户选择进入哪个世界 生成还是读取
        根据用户的输入 生成并返回一个世界
        
        该功能有待GUI窗口化
    """

    def world_create(self):
        # 通过世界类型名得到相应的世界生成器
        def get_generator(generator_file):
            generator_file = 'world.world_project.' + generator_file + '.' + 'world_generator'

            try:
                generator_module = importlib.import_module(generator_file)

            except ModuleNotFoundError:
                # can not find this type of world
                return None

            return generator_module.Concrete_world_generator()

        # 使用世界生成器参数化生成世界
        # map_size规定了有 几行（高 纵坐标） 和 几列（宽 横坐标）
        def get_world(generator, maximum_height=30, map_size=(50, 100),
                      animals_para="random_animals", plants_para="random_plants",
                      obj_para="random_obj",
                      water_para="default_water",
                      landform_para="default_landform",
                      terrain_para="default_terrain"):
            # 输入参数为 地形类型的数量 地图大小 生物生成参数 物品生成参数
            return generator.generate_a_world(maximum_height=maximum_height, map_size=map_size,
                                              animals_para=animals_para, plants_para=plants_para,
                                              obj_para=obj_para, water_para=water_para,
                                              landform_para=landform_para, terrain_para=terrain_para)

        # 读取命令 这个也可以用前端干
        # 选择世界进入模式
        # entry_mode = input("Please choose world mode(generate or load): ")
        # while entry_mode not in ["generate", "load"]:
        #     entry_mode = input("Input is illegal, please try again(generate or load): ")

        # entry_mode = "load"
        entry_mode = "generate"

        # 根据世界类型获取世界生成器
        self.generator = get_generator(self.world_type_name)
        while self.generator is None:
            self.world_type_name = input("can not find this type of world, please input other world type name: ")
            self.generator = get_generator(self.world_type_name)

        """
            
        """
        world = None
        # 如果生成一个世界
        if entry_mode == "generate":
            # 通过世界生成器生成世界
            world = get_world(self.generator)

        # 读档一世界
        elif entry_mode == "load":
            world_name = input("Please input world name: ")
            while world is None:
                try:
                    # 通过读档器读取世界
                    world = self.load(self.world_type_name, world_name)
                except FileNotFoundError:
                    world = None
                    world_name = input("Can't find this file, Please correct input and input world name again: ")

        return world

    """
        ======================
            openAI环境方法
        ======================
    """
    # 世界运作
    def step(self, action):
        print(action)
        self.world.take_action(self.world.translate_openai_command_to_mteac(self.world.state, action))
        return self.world.translate_mteac_state_to_openai(self.world.state), 0, False, None

    """
        世界每运行一轮都会调用一次该方法 统计和可视化在这里进行
    """

    # 后续拓展
    def render(self, mode="ai"):
        # 可视化 读入状态 由状态类实现 地形地图和生物列表 然后可视化
        # 关闭时返回False
        def visualization():
            return self.exhibitor.display(mode)

        # 终端「可视化」输出
        # for map_line in self.state.get_map():
        #     print(map_line)
        # self.state.print_show_creature()

        return visualization()

    def reset(self):
        self.world.evolution()
        return self.world.translate_mteac_state_to_openai(self.world.state)

    def seed(self, seed=None):
        pass

    def close(self):
        pass


    """
        ======================
            游戏模式方法
        ======================
        目前仅仅对mesh_world有效
        类变量play_mode定义了是否可以进行game_mode
    """
    def game_mode(self):
        """
            让世界不断运作的死循环 除非后台要求退出或程序被x掉
        """
        # 世界不断运作
        def world_evolution():
            self.player_cmd = self.render("normal")
            print("玩家指令为: ", self.player_cmd)
            # 用gate判断是否结束
            while self.gate:
                print("世界开始运作一次")
                self.world.take_action(self.player_cmd)
                self.world.evolution()
                print("世界运作结束")
                # 可视化等操作
                self.player_cmd = self.render("normal")
                print("玩家指令为: ", self.player_cmd)
                if not self.player_cmd:
                    self.gate = False

        """
            终端后台 用户可以输入指令来控制程序
                目前的指令有：
                    quit: 退出程序
                            目前有瑕疵 需要玩家移动一格才会真的退出
                            另一个瑕疵 玩家叉掉程序以后 input会滞留
                    save 存档名: 保存当前世界到【存档名.save】文件中 
        """
        # 后台
        def background():
            if self.world.backgroundable:
                while self.gate:
                    background_cmd = input("Please input command: \n")

                    cmd = background_cmd.split(' ')
                    if cmd[0] == "quit":
                        self.gate = False
                        self.exhibitor.set_out()
                        break
                    elif cmd[0] == "save":
                        if len(cmd) == 1:
                            cmd.append('save')
                        self.save(cmd[1])
                    elif cmd[0] == "stat":
                        if self.world.statistical:
                            try:
                                print(self.world.statistics(cmd))
                            except ValueError:
                                print("The parameter format is incorrect, please check the parameters and input again")
                        else:
                            print("The program is not statistical.")
                    else:
                        print("wrong command,please check and input again")
            else:
                print("The world has no background function.")

        """
            游戏模式下的世界运作
        """
        # 如果世界生成成功 则进入该世界 否则退出程序
        if self.world:
            if self.world.play_mode:
                print("世界创建成功")
                # 初始化线程和运行门 后台线程和主线程同步进行
                self.background_thread = threading.Thread(target=background)
                # 初始化用户操作并规定程序是否允许
                self.player_cmd = 1
                self.gate = True

                """
                    两个线程
                """
                # 后台和世界开始不停运作
                self.background_thread.setDaemon(True)
                print("创建后台")
                self.background_thread.start()
                print("世界开始运作")
                world_evolution()
            else:
                print("该世界方案无玩家模式")
        else:
            print("世界创建失败")

    """
        当玩家调用并指定存档名后会调用File_processor对象进行存档 将当前世界以json格式存在save文件夹中
        具体功能由File_processor对象实现
        
        后台存档指令格式: save 存档名
    """

    # 存档
    def save(self, file_name):
        print("正在存档...")
        world_type_name = type(self.world).__name__
        state = self.world.get_state()
        File_processor.archive(state, world_type_name, file_name)

    """
        读档 指定存档 读取后覆盖当前世界
        具体功能由File_processor对象实现
        输入:
            world_type_name 世界类型
            file_name       存档名
        返回一个世界对象
    """

    # 读档
    def load(self, world_type_name, file_name):
        print("正在读档...")
        state = File_processor.load(world_type_name, file_name)
        world = self.generator.generate_a_world_by_state(state)
        return world
