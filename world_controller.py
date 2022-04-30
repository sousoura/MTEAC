import importlib
import threading
from world.world_project.mesh_world.file_processor import File_processor
from world.world_project.mesh_world.exhibitor import Exhibitor


# 控制整个程序的进程
class World_controller:
    def __init__(self):
        # 整个程序的起点

        # 生成世界
        """
            用户选择进入哪个世界 生成还是读取
        """
        self.generator = None
        self.world = self.entry()

        # 可视化创建
        self.exhibitor = Exhibitor(self.world, (1000, 1000))

        # 如果世界生成成功 则进入该世界 否则退出程序
        if self.world:
            # 初始化线程和运行门 后台线程和主线程同步进行
            self.background_thread = threading.Thread(target=self.background)
            # 初始化用户操作并规定程序是否允许
            self.player_cmd = 1
            self.gate = True

            # 后台和世界开始不停运作
            self.background_thread.start()
            self.world_evolution()

    # 程序入口
    """
        用户选择进入哪个世界 生成还是读取
    """
    def entry(self):
        # 通过世界类型名得到相应的世界生成器
        def get_generator(generator_file):
            generator_file = 'world.world_project.' + generator_file + '.' + 'world_generator'
            generator_module = importlib.import_module(generator_file)
            # from world.mesh_world.mesh_world_generator import Concrete_world_generator as Generator
            return generator_module.Concrete_world_generator()

        # 使用世界生成器参数化生成世界
        def get_world(generator, terrain_num=3, map_size=(25, 25), creature_parameter="random_creature",
                      obj_parameter="random_obj"):
            # 输入参数为 地形类型的数量 地图大小 生物生成参数 物品生成参数
            return generator.generate_a_world(terrain_num, map_size, creature_parameter, obj_parameter)

        # 读取命令 这个也可以用前端干
        entry_mode = input("Please choose world mode(generate or load): ")
        world = None
        # 如果生成一个世界
        if entry_mode == "generate":
            """
                待改进： 可以进一步询问生成参数
            """
            world_type_name = input("Please input world type name: ")
            # 根据世界类型生成世界
            self.generator = get_generator(world_type_name)
            # 通过世界生成器生成世界
            world = get_world(self.generator)
        elif entry_mode == "load":
            world_type_name = input("Please input world type name: ")
            world_name = input("Please input world name: ")
            self.generator = get_generator(world_type_name)
            world = self.load(world_type_name, world_name)

        return world

    # 世界不断运作
    def world_evolution(self):
        self.player_cmd = self.expansion()
        # 用gate判断是否结束
        while self.gate:
            self.world.evolution(self.player_cmd)
            # 可视化等操作
            self.player_cmd = self.expansion()
            if not self.player_cmd:
                self.gate = False

    # 后台
    def background(self):
        while self.gate:
            background_cmd = input("Please input command: ")

            cmd = background_cmd.split(' ')
            if cmd[0] == "quit":
                self.gate = False
                break
            elif cmd[0] == "save":
                self.save(cmd[1])

    # 后续拓展
    def expansion(self):
        # 「可视化」输出
        # for map_line in self.state.get_map():
        #     print(map_line)
        # self.state.print_show_creature()

        return self.visualization()

    # 可视化 读入状态 由状态类实现 地形地图和生物列表 然后可视化
    # 关闭时返回False
    def visualization(self):
        return self.exhibitor.display(self.world)

    # 存档
    def save(self, file_name):
        world_type_name = type(self.world).__name__
        state = self.world.get_state()
        File_processor.archive(state, world_type_name, file_name)

    # 读档
    def load(self, world_type_name, file_name):
        state = File_processor.load(world_type_name, file_name, self.generator)
        world = self.generator.generate_a_world_by_state(state)
        return world
