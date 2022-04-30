import json
import os
from world.world_project.mesh_world.entity.mesh_entities import *
from world.world_project.mesh_world.entity.creature.animal.human.human_brain import Human_brain


"""
    文件处理类
    读档和存档之类的 所有和储存读取相关的都在这类
"""


class File_processor:
    # 存档
    @classmethod
    def archive(cls, state, world_type_name, file_name):
        # 将state转换为json的可读的字典的配适函数
        def state_obj_to_json(state_obj):
            return {
                "terrain": state_obj.get_terrain(),
                "terrain_size": state_obj.get_terrain_size(),
                "creatures": creatures_list_to_json(state.get_creatures()),
                "objects": state.get_objects(),
            }

        # 将生物列表转换为json可读的字典的配适盘数
        """
            格式为 生物物种名: [{单个生物的属性}, {单个生物的属性}...]
        """
        def creatures_list_to_json(creatures):
            goal_dict = {}
            for creature in creatures:
                if type(creature).__name__ in goal_dict:
                    goal_dict[type(creature).__name__].append(creature_obj_to_json(creature))
                else:
                    goal_dict[type(creature).__name__] = [creature_obj_to_json(creature)]
            return goal_dict

        # 将单个生物转换为json可读的字典的配适盘数
        def creature_obj_to_json(creature):
            return {
                "position": creature.get_position(),
                "life": creature.get_life(),
            }

        path = os.getcwd()  # 获取当前路径
        with open(path + "\\" + "world\\world_project" + "\\" + world_type_name +
                  "\\save\\" + file_name + ".json", "w+") as save_file:
            json.dump(state, save_file, default=state_obj_to_json, sort_keys=True, indent=4)

        print("Successful archive.")

    @classmethod
    def load(cls, world_type_name, file_name, generator):
        # 读取json字典的内容并结构化创建对象
        def json_to_state_obj(json_dict):
            terrain = json_dict["terrain"]
            terrain_size = tuple(json_dict["terrain_size"])
            creature_list = []
            for species_name in json_dict["creatures"]:
                for creature_individual_dict in json_dict["creatures"][species_name]:
                    species = globals()[species_name]
                    """
                        待修复：human brain没有存档 这里临时新生成一个
                    """
                    species_instance = \
                        species(creature_individual_dict["position"], creature_individual_dict["life"], Human_brain())
                    creature_list.append(species_instance)
            obj_list = json_dict["objects"]
            return generator.building_a_state(terrain, terrain_size, creature_list, obj_list)

        # 读取json存档文件内容
        path = os.getcwd()  # 获取当前路径
        with open(path + "\\" + "world\\world_project" + "\\" + world_type_name +
                  "\\save\\" + file_name + ".json", "r") as save_file:
            json_str = save_file.read()

        # json字符串转为字典
        json_dict = json.loads(json_str)

        # 根据字典结构化创建状态对象
        state = json_to_state_obj(json_dict)

        print("Successful load.")
        return state
