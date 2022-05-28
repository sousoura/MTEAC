import json
import pygame

json_table_textuure = "TextureTable.json"



class TextureTable:
    
    #初始化: 声明成员变量, 加载纹理表
    def __init__(self, table_path):
        self.key_sexture = "surface"    #纹理的surface, 未加载时为None
        self.key_filepath = "filepath"  #纹理的文件路径
        self.key_explain = "explain"    #纹理的说明文本(u8)
        self.table_texture = None       #纹理表
        
        with open(json_table_textuure, "r") as f:
            self.table_texture = json.loads(f.read())
    
    #加载一个纹理, 通过纹理id加载
    def LoadTexture(self, id):
        self.table_texture[id][self.key_sexture] = pygame.image.load(
            self.table_texture[id][self.key_filepath])
        return self.table_texture[id][self.key_sexture]
    
    #获取纹理, 通过纹理id获取纹理surfase
    def GetTexture(self, id):
        if self.table_texture[id][self.key_sexture] == None:
            self.LoadTexture(id)
        return self.table_texture[id][self.key_sexture]
    
    #将纹理表全部加载
    def LoadAll(self):
        for texture in self.table_texture.keys():
            self.LoadTexture(texture)
    
    #向纹理表添加纹理
    def AddTexture(self, id, filepath, explain=""):
        temp = {
            id:{
                self.key_explain: explain,
                self.key_filepath: filepath,
                self.key_surface: None
                }
            }
        self.table_texture.append(temp)
    
    
    