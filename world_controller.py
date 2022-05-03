import importlib
import threading
from world.file_processor import File_processor
from world.world_project.mesh_world.exhibitor import Exhibitor


"""
    代表MTEAC程序的类
    负责的功能：
        程序的入口
        整个程序的不断运行
        输入输出：窗口化显示 后台
"""


# 控制整个程序的进程
class World_controller:

    """
        程序入口 让用户做初始化选择
        让程序不断运作下去
        分为两个线程
            程序和窗口线程
            后台命令线程
    """
    def __init__(self):
        self.generator = None

        # 整个程序的起点
        # 生成世界
        """
            用户选择进入哪个世界 生成还是读取
        """
        self.world = self.entry()

        """
            Exhibitor负责窗口的可视化呈现
        """
        # 创建可视化窗口 后面那个元组是世界的框的大小而不是窗口大小 窗口还会更高一点因为要有状态栏
        self.exhibitor = Exhibitor(self.world, (800, 800))

        # 如果世界生成成功 则进入该世界 否则退出程序
        if self.world:
            # 初始化线程和运行门 后台线程和主线程同步进行
            self.background_thread = threading.Thread(target=self.background)
            # 初始化用户操作并规定程序是否允许
            self.player_cmd = 1
            self.gate = True

            """
                两个线程
            """
            # 后台和世界开始不停运作
            self.background_thread.start()
            self.world_evolution()

    # 程序入口
    """
        负责用户的初始化选择
        用户选择进入哪个世界 生成还是读取
        根据用户的输入 生成并返回一个世界
        
        该功能有待GUI窗口化
    """
    def entry(self):
        # 通过世界类型名得到相应的世界生成器
        def get_generator(generator_file):
            generator_file = 'world.world_project.' + generator_file + '.' + 'world_generator'
            generator_module = importlib.import_module(generator_file)
            # from world.mesh_world.mesh_world_generator import Concrete_world_generator as Generator
            return generator_module.Concrete_world_generator()

        # 使用世界生成器参数化生成世界
        def get_world(generator, maximum_height=30, map_size=(50, 50),
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
        # entry_mode = input("Please choose world mode(generate or load): ")
        # entry_mode = "generate"
        entry_mode = "load"
        world = None
        # 如果生成一个世界
        if entry_mode == "generate":
            """
                待改进： 可以进一步询问生成参数
            """
            # world_type_name = input("Please input world type name: ")
            world_type_name = "mesh_world"
            # 根据世界类型生成世界
            self.generator = get_generator(world_type_name)
            # 通过世界生成器生成世界
            world = get_world(self.generator)
        elif entry_mode == "load":
            world_type_name = input("Please input world type name: ")
            # world_type_name = "mesh_world"
            world_name = input("Please input world name: ")
            self.generator = get_generator(world_type_name)
            world = self.load(world_type_name, world_name)

        return world

    """
        让世界不断运作的死循环 除非后台要求退出或程序被x掉
    """
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

    """
        终端后台 用户可以输入指令来控制程序
            目前的指令有：
                quit: 退出程序
                        目前有瑕疵 需要玩家移动一格才会真的退出
                        另一个瑕疵 玩家叉掉程序以后 input会滞留
                save 存档名: 保存当前世界到【存档名.json】文件中 
    """
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
            elif cmd[0] == "stat":
                print(self.statistics(cmd))

    """
        世界每运行一轮都会调用一次该方法 统计和可视化在这里进行
    """
    # 后续拓展
    def expansion(self):
        # 可视化 读入状态 由状态类实现 地形地图和生物列表 然后可视化
        # 关闭时返回False
        def visualization():
            return self.exhibitor.display(self.world)

        # 终端「可视化」输出
        # for map_line in self.state.get_map():
        #     print(map_line)
        # self.state.print_show_creature()

        return visualization()

    """
        当玩家调用并指定存档名后会调用File_processor对象进行存档 将当前世界以json格式存在save文件夹中
        具体功能由File_processor对象实现
    """
    # 存档
    def save(self, file_name):
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
        state = File_processor.load(world_type_name, file_name)
        world = self.generator.generate_a_world_by_state(state)
        return world

    """
        统计数据 指定要统计的数据类型 筛选条件的分类 具体筛选条件（以数组形式）
        数据类型：num, avg_life
        筛选条件的分类，用哈夫曼编码：
            物种为1;
            生命值为2;
            饥饿值为4;
            位置为8.
        具体筛选条件以物种、生命值、饥饿值、位置的顺序排序，如没有则不用填，其中生命值、饥饿值为具体数值，位置暂时留在这里，尚未开发
        例如:
            stat num 3 Human_being 5  为查询生命值为5的人类的个数
            stat num 1 Human_being 为查询人类的个数
    """
    # 统计数据
    def statistics(self, cmd):
        # 这里默认了所有世界都有生物
        creatures = self.world.state.animals + self.world.state.plants
        num = 0
        sum_life = 0
        for creature in creatures:
            pos = len(cmd) - 1
            # 对于未死亡的生物，进行大量的筛选
            if not creature.is_die():
                cmd_num = int(cmd[2])
                if cmd_num >= 8:
                    cmd_num -= 8
                    # 进行位置的相关筛选
                    pos -= 1
                if cmd_num >= 4:
                    cmd_num -= 4
                    # 进行饥饿值的相关筛选
                    pos -= 1
                if cmd_num >= 2:
                    cmd_num -= 2
                    # 进行生命值的相关筛选
                    if creature.life != int(cmd[pos]):
                        continue
                    pos -= 1
                if cmd_num >= 1:
                    cmd_num -= 1
                    # 进行物种的相关筛选
                    if type(creature).__name__ != cmd[pos]:
                        continue

            # 走到这里，就完成了筛选
            num += 1
            if cmd[1] == "avg_life":
                sum_life += creature.life

        # 完成了遍历
        if cmd[1] == "avg_life":
            return sum_life/num
        return num



