import tkinter as PlayerViewGui
import pygame, sys, json, math


#                                                             #
# {                                                           #
#     "FileType": "TextureTable",                             # 文件类型标识
#     "DirMapping": {                                         # 路径映射表
#         "Texturt": "ART/Texture"                            # 将Texturt映射至路径ART/Texture
#     },                                                      #
#     "TextureTable": {                                       # 纹理表
#         "0": {                                              # id
#             "name": "\u8349",                               # 说明文本(utf-8)
#             "filepath": "Texturt:Surface/Grassland1.png"    # 文件路径, 从工作路径出发(utf-8)
#         },                                                  # 编写时可省略, 保存文件自动生成
#         "1": {                                              #
#             "name": "\u6c99",                               #
#             "filepath": "Texturt:Surface/desert.png"        #
#         },                                                  #
#         "2": {                                              #
#             "name": "\u6c34",                               #
#             "filepath": "Texturt:Surface/Water.png"         #
#         }                                                   #
#     }                                                       #
# }                                                           #
#                                                             #

class TextureTable:
    # 所有传入id均需为str类型
    # table_path: 纹理表文件路径
    # pygame: 包
    # 初始化: 声明成员变量, 加载纹理表
    def __init__(self, table_path, pygame):
        self.pygame = pygame
        self.key_FileType = "FileType"  # 键_文件类型标注
        self.key_TextureTable = "TextureTable"  # 键_纹理表
        self.key_DirMapping = "DirMapping"  # 键_路径映射
        self.key_sexture = "surface"  # 键_纹理surface, 未加载时为None
        self.key_filepath = "filepath"  # 键_纹理文件路径(u8)
        self.key_name = "name"  # 键_纹理名(u8)
        self.mapping_json = None  # 纹理表文件所有内容
        self.mapping_dirmapping = None  # 路径映射表
        self.table_texture = None  # 纹理表

        with open(table_path, "r") as f:
            self.mapping_json = json.loads(f.read())
        self.mapping_dirmapping = self.mapping_json[self.key_DirMapping]
        self.table_texture = self.mapping_json[self.key_TextureTable]

        for data in self.table_texture.values():
            if not self.key_sexture in data:
                data[self.key_sexture] = None

    # 加载一个纹理, 通过纹理id加载, 返回加载的surface
    def LoadTexture(self, id: str):
        filepath_full = ""
        if ":" in self.table_texture[id][self.key_filepath]:
            dir_and_path = self.table_texture[id][self.key_filepath].split(":")
            filepath_full = self.mapping_dirmapping[dir_and_path[0]] + "/" + dir_and_path[1]
        self.table_texture[id][self.key_sexture] = self.pygame.image.load(filepath_full)
        # print(filepath_full)
        return self.table_texture[id][self.key_sexture]

    # 获取纹理, 通过纹理id获取纹理surfase
    def GetTexture(self, id: str):
        if self.table_texture[id][self.key_sexture] == None:  # 若未加载则加载该纹理
            self.LoadTexture(id)
        return self.table_texture[id][self.key_sexture]

    # 获取纹理名
    def GetName(self, id: str):
        return self.table_texture[id][self.key_name]

    # 获取路径映射表
    def GetDirMapping(self):
        return self.mapping_dirmapping

    # 将纹理表全部加载
    def LoadAll(self):
        for id in self.table_texture.keys():
            self.LoadTexture(id)

    # 向纹理表添加纹理
    def AddTexture(self, id: str, filepath, name=""):
        temp = {
            id: {
                self.key_name: name,
                self.key_filepath: filepath,
                self.key_surface: None
            }
        }
        self.table_texture.append(temp)

    # 根据id获取一个纹理的数据(不推荐)
    def GetData(self, id: str):
        return self.table_texture[id]

    # 获取整个纹理表(强烈不推荐)
    def GetTable(self):
        return self.table_texture

    # 保存纹理表数据
    def SaveTable(self, save_path):
        if self.table_texture != None:
            with open(save_path, "w+") as file:
                json.dump(self.table_texture, file)


cubeSize = 64


class PlayerView():
    def __init__(self):
        self.canvas = pygame.display.get_surface()
        # print(type(self.canvas))
        self.surfaceFullMap = None
        self.landform_map = None
        self.HeightMap = None
        self.water_map = None
        self.animals_position = None
        self.plants_position = None
        self.objs_position = None
        self.player_controlling_unit = None
        self.TextureTable1 = TextureTable("world/Texture/TextureTable.json", pygame)
        # self.player_view(self.terrainMap, self.TextureTable1)
        self.win_size = None
        self.landformLastTurn = None  # 上回合的地形
        self.b = None

        self.camera_top_left = [0, 0]

    def set_landform_map(self, landform_map):
        if self.landform_map == None or self.landform_map != landform_map:
            self.landform_map = landform_map

    '''       
    def set_camera_topleft(self, player_At):
        print(len(self.landform_map))
        #动物坐标加上摄像机范围的一半即为摄像机左上角的坐标吧
        #如果角色在地图的边缘就不能居中了
        print(["现在玩家所处的位置：", str(player_At)])
        #player_At[0]好像是y轴??
        if player_At[0] - 7 < 0:
            self.camera_top_left[0] = 0
        elif player_At[0] + 7 > len(self.landform_map):
            self.camera_top_left[0] = len(self.landform_map) - 14
        else: 
            self.camera_top_left[0] = player_At[0] - 7
        print(["现在摄像机的左上角：", str(self.camera_top_left)])
        
        if player_At[1] - 12 < 0:
            self.camera_top_left[1] = 0
        elif player_At[1] + 12 > len(self.landform_map[0]):
            self.camera_top_left[1] = len(self.landform_map[0]) - 24
        else:
            self.camera_top_left[1] = player_At[1] - 11
        #print(self.camera_top_left)
    '''

    def set_camera_topleft(self, camera_focus):
        # 24, 14
        windowWidth_grid = int(self.win_size[0] / cubeSize)
        windowHight_grid = int(self.win_size[1] / cubeSize)

        self.camera_top_left[0] = camera_focus[0] - windowHight_grid / 2
        self.camera_top_left[1] = camera_focus[1] - windowWidth_grid / 2

        worldWidth_grid = len(self.landform_map[0])
        worldHight_grid = len(self.landform_map)

        if self.camera_top_left[1] < 0:
            self.camera_top_left[1] = 0
        elif self.camera_top_left[1] > worldWidth_grid - windowWidth_grid:
            self.camera_top_left[1] = worldWidth_grid - windowWidth_grid

        if self.camera_top_left[0] < 0:
            self.camera_top_left[0] = 0
        elif self.camera_top_left[0] > worldHight_grid - windowHight_grid:
            self.camera_top_left[0] = worldHight_grid - windowHight_grid

        # print("win_size_grid: " + str(windowWidth_grid) + ", " + str(windowHight_grid))
        # print("location_player: " + str(camera_focus[0]) + ", " + str(camera_focus[1]))
        # print("\tlocation_camera: " + str(self.camera_top_left[0]) + ", " + str(self.camera_top_left[1]))

    def set_camera_topleft_Ai(self, directionPressed):
        self.camera_top_left = directionPressed

    def draw_landform(self, landform_map, HeightMap, TextureTable1):
        if self.landformLastTurn != landform_map:
            terrain = landform_map

            for x in range(0, len(terrain)):
                for y in range(len(terrain[x])):

                    current = HeightMap[x][y]

                    self.surfaceFullMap.blit(TextureTable1.GetTexture(str(terrain[x][y])), (y * cubeSize, x * cubeSize))

                    # 这三行用来显示每个格的高度，太丑了就先注释掉了
                    # font = pygame.font.SysFont("Times", 30)
                    # heightNumber = font.render(str(current), True, (0, 0, 0))
                    # self.surfaceFullMap.blit(heightNumber, (y * cubeSize, x * cubeSize))

                    list1 = [0, 0, 0, 0]  ##悬崖用旋转90，180 270度的同一张贴图表示，所以四个数字分别是上，左， 下，右

                    # 上up
                    if x == 0:
                        list1[0] = 0
                    else:
                        list1[0] = current - HeightMap[x - 1][y]
                    # 左left
                    if y == 0:
                        list1[1] = 0
                    else:
                        list1[1] = current - HeightMap[x][y - 1]
                    # 下down
                    if x == len(HeightMap) - 1:
                        list1[2] = 0
                    else:
                        list1[2] = current - HeightMap[x + 1][y]
                    # 右right
                    if y == len(HeightMap[x]) - 1:
                        list1[3] = 0
                    else:
                        list1[3] = current - HeightMap[x][y + 1]

                    for i in range(0, len(list1)):
                        route = 90
                        if list1[i] > 0:
                            try:
                                cilffTexture = pygame.transform.rotate(
                                    TextureTable1.GetTexture("cliff_" + str(list1[i])), route * i)
                            except:
                                cilffTexture = pygame.transform.rotate(TextureTable1.GetTexture("cliff_5"), route * i)
                            self.surfaceFullMap.blit(cilffTexture, (y * cubeSize, x * cubeSize))
            self.landformLastTurn = landform_map
            self.b = self.surfaceFullMap.copy()
        else:
            # self.surfaceFullMap = self.b
            self.surfaceFullMap.blit(self.b, (0, 0))
            # self.surfaceFullMap.blit(self.b, (0, 0))尝试了一下这个，结果输入指令之后屏幕不刷新了- -

    def draw_water(self):
        rows_num = len(self.water_map)
        cols_num = len(self.water_map[0])

        for i in range(0, rows_num):
            # print("aaaa is :" + str(key))
            # 现在key是元组
            for j in range(0, cols_num):  # 现在i是list，遍历list里面的东西的type
                # print(type(i).__name__)
                if self.water_map[i][j] > 0:
                    pass

                    """
                        # 老刁version
                    """
                    # waterTexture = self.TextureTable1.GetTexture(str(7))
                    # waterTexture.set_alpha((self.water_map[i][j] * 0.1 + 1) * 100)
                    # # print(math.ceil(self.water_map[i][j] / 10))
                    # self.surfaceFullMap.blit(waterTexture, (j * cubeSize, i * cubeSize))

                    """
                        吴忧version
                    """
                    water_surface = \
                        pygame.Surface(
                            (64, 64)
                            , pygame.SRCALPHA, 32)

                    water_surface.fill((0, 0, 255, max(0, min(self.water_map[i][j] / (1 + 5) * 200, 255))))
                    self.surfaceFullMap.blit(water_surface, (j * cubeSize, i * cubeSize))

                    pass

    def draw_amimal(self, animals_position, TextureTable1):

        for key in animals_position.keys():
            # print("aaaa is :" + str(key))
            # 现在key是元组
            for i in animals_position[key]:  # 现在i是list，遍历list里面的东西的type
                # print(type(i).__name__)
                self.surfaceFullMap.blit(TextureTable1.GetTexture(str(type(i).__name__)),
                                         (key[1] * cubeSize, key[0] * cubeSize))
                # print(self.surfaceFullMap.get_width(), self.surfaceFullMap.get_height())

    def draw_plants(self, plants_position, TextureTable1):
        for key in plants_position.keys():
            # print("aaaa is :" + str(key))
            # 现在key是元组
            for i in plants_position[key]:  # 现在i是list，遍历list里面的东西的type
                # print(type(i).__name__)
                self.surfaceFullMap.blit(TextureTable1.GetTexture(str(type(i).__name__)),
                                         (key[1] * cubeSize, key[0] * cubeSize))
                # print(self.surfaceFullMap.get_width(), self.surfaceFullMap.get_height())

    def draw_objects(self, objs_position, TextureTable1):
        for key in objs_position.keys():
            # print("aaaa is :" + str(key))
            # 现在key是元组
            for i in objs_position[key]:  # 现在i是list，遍历list里面的东西的type
                # print(type(i).__name__)
                self.surfaceFullMap.blit(TextureTable1.GetTexture(str(type(i).__name__)),
                                         (key[1] * cubeSize, key[0] * cubeSize))
                # print(self.surfaceFullMap.get_width(), self.surfaceFullMap.get_height())

    def ReceiveVariable(self, landFormMap, animals_position, plants_position, objs_position, HeightMap, win_size,
                        water_map):
        self.win_size = win_size
        self.landform_map = landFormMap
        # self.set_camera_topleft(player_At)

        self.water_map = water_map
        # print(self.water_map)
        # 经测试后发现：在只画生物的情况下，若不每次都重新生成mapsurfaceFullMap，则动一次之后上一次的还在，就像那个死机屏幕一样
        self.surfaceFullMap = pygame.Surface(size=(len(landFormMap[0]) * cubeSize, len(landFormMap) * cubeSize))

        self.landform_map = landFormMap
        self.HeightMap = HeightMap

        self.animals_position = animals_position
        self.plants_position = plants_position
        self.objs_position = objs_position

    def Update(self):
        self.draw_landform(self.landform_map, self.HeightMap, self.TextureTable1)
        self.draw_plants(self.plants_position, self.TextureTable1)
        self.draw_water()  # 画水之后会非常的卡，，，，
        self.draw_objects(self.objs_position, self.TextureTable1)
        self.draw_amimal(self.animals_position, self.TextureTable1)
        self.canvas = pygame.display.get_surface()
        self.canvas.blit(self.surfaceFullMap, (0, 0), (
        self.camera_top_left[1] * cubeSize, self.camera_top_left[0] * cubeSize, self.win_size[0] + 64,
        self.win_size[1] + 64))
        # 左上角摄像机的坐标

    '''
    单位指令：
    Z: eat
    X: attack
    C: drink
    V: rest
    A: pick_up
    S: put_down
    '''

    '''
    def ReceiveVariable(self):
        self.player_view(self.landform_map, self.TextureTable1)
    '''


'''
while 1:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player_view(list1)
    pygame.display.update()
'''
