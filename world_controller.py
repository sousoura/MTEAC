import importlib
import threading
from world.world_project.mesh_world.file_processor import File_processor


class World_controller:
    generator = None

    def __init__(self):
        # 生成世界
        self.world = self.entry()
        if self.world:
            # 初始化线程和运行门
            self.background_thread = threading.Thread(target=self.background)
            self.player_cmd = 1
            self.gate = True

            # 世界开始不停运作
            self.background_thread.start()
            self.world_evolution()

    def entry(self):
        entry_mode = input("Please choose world mode(generate or load): ")
        # entry_mode = 'generate'
        world = None
        if entry_mode == "generate":
            world_type_name = input("Please input world type name: ")
            # world_type_name = "mesh_world"
            # 根据世界类型生成世界
            # generator = self.get_generator("mesh_world")
            self.generator = self.get_generator(world_type_name)
            # 通过世界生成器生成世界
            world = self.get_world(self.generator)
        elif entry_mode == "load":
            world_type_name = input("Please input world type name: ")
            world_name = input("Please input world name: ")
            self.generator = self.get_generator(world_type_name)
            world = self.load(world_type_name, world_name)

        return world

    # 通过世界类型名得到相应的世界生成器
    def get_generator(self, generator_file):
        generator_file = 'world.world_project.' + generator_file + '.' + 'world_generator'
        generator_module = importlib.import_module(generator_file)
        # from world.mesh_world.mesh_world_generator import Concrete_world_generator as Generator
        return generator_module.Concrete_world_generator()

    def get_world(self, generator):
        # 世界生成器生成世界
        # 输入参数为 地形类型的数量 地图大小 生物生成参数 物品生成参数
        return generator.generate_a_world(2, (5, 5), "random_creature", "random_obj")

    def world_evolution(self):
        self.player_cmd = self.world.expansion()
        # 用gate判断是否结束
        while self.gate:
            self.world.evolution(self.player_cmd)
            self.player_cmd = self.world.expansion()
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
