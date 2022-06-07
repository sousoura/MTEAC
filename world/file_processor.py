import json
import os
from world.world_project.mesh_world.entity.mesh_entities import *
from world.entity.entity_import import *

"""
    文件处理类
        实现了默认的存档和读档功能
        职能：读档和存档之类的 所有和储存读取相关的都在这类
        已经实现泛化和自动化
        （该逻辑待优化）
"""


class File_processor:
    """
        实例存档器
    """

    # 存档
    @classmethod
    def archive(cls, state, world_type_name, file_name):
        """
            state:              某个world project 的state实例 该实例存有所有世界此刻的状态的信息
            world_type_name:    world project的名字 格式同MTEAC类中的self.world_type_name
            file_name:          存档文件的名称 不需要加后缀 存档成功后 存档文件会出现在world project的save文件夹下
        """
        def state_obj_to_json(state_obj):
            new_dict = instance_archiver(state_obj)
            return new_dict

        def instance_archiver(state):
            return instance_json_ise(state)

        def instance_json_ise(instance):
            class_name = type(instance).__name__
            instance_dict = {}
            for attribute_name in instance.__dir__():
                # 排除内置方法和属性
                if attribute_name[0] != "_":
                    # 排除方法对象
                    if not hasattr(getattr(instance, attribute_name), '__call__'):
                        # 判断直接可json性
                        if isinstance(getattr(instance, attribute_name), (int, str, float, bool)):
                            instance_dict[attribute_name] = getattr(instance, attribute_name)
                        elif getattr(instance, attribute_name) is None:
                            instance_dict[attribute_name] = None
                            # 若为数组 元组或字典
                        elif isinstance(getattr(instance, attribute_name), list):
                            instance_dict[attribute_name] = list_json_ise(getattr(instance, attribute_name))
                        elif isinstance(getattr(instance, attribute_name), tuple):
                            instance_dict[attribute_name] = tuple_json_ise(getattr(instance, attribute_name))
                        elif isinstance(getattr(instance, attribute_name), dict):
                            instance_dict[attribute_name] = dict_json_ise(getattr(instance, attribute_name))
                        # 若为实例
                        else:
                            instance_dict[attribute_name] = \
                                {type(getattr(instance, attribute_name)).__name__: instance_json_ise(
                                    getattr(instance, attribute_name))}
            return instance_dict

        def list_json_ise(in_list):
            tem_list = []
            for ele in in_list:
                if isinstance(ele, (int, str, float, bool)):
                    tem_list.append(ele)
                # None 处理
                elif ele is None:
                    tem_list.append(list_json_ise(None))
                # 若为数组 元组或字典
                elif isinstance(ele, list):
                    tem_list.append(list_json_ise(ele))
                elif isinstance(ele, tuple):
                    tem_list.append(tuple_json_ise(ele))
                elif isinstance(ele, dict):
                    tem_list.append(dict_json_ise(ele))
                # 若为实例
                else:
                    tem_list.append({type(ele).__name__: instance_json_ise(ele)})
            return tem_list

        def tuple_json_ise(in_tuple):
            return tuple(list_json_ise(in_tuple))

        def dict_json_ise(in_dict):
            tem_dict = {}
            for key in in_dict:
                key_type = key
                if isinstance(key, tuple):
                    key_type = str(key)
                if isinstance(in_dict[key], (int, str, float, bool)):
                    tem_dict[key_type] = in_dict[key]
                elif in_dict[key] is None:
                    tem_dict[key_type] = None
                # 若为数组 元组或字典
                elif isinstance(in_dict[key], list):
                    tem_dict[key_type] = list_json_ise(in_dict[key])
                elif isinstance(in_dict[key], tuple):
                    tem_dict[key_type] = tuple_json_ise(in_dict[key])
                elif isinstance(in_dict[key], dict):
                    tem_dict[key_type] = dict_json_ise(in_dict[key])
                # 若为实例
                else:
                    tem_dict[key_type] = {type(in_dict[key]).__name__: cls.instance_json_ise(in_dict[key])}
            return tem_dict

        path = os.getcwd()  # 获取当前路径
        with open(path + "\\" + "world\\world_project" + "\\" + world_type_name +
                  "\\save\\" + file_name + ".save", "w+") as save_file:
            # json.dump(state, save_file, default=state_obj_to_json, sort_keys=True, indent=4)
            state_dic = state_obj_to_json(state)
            # print(state_dic)
            json.dump(state_dic, save_file, sort_keys=True, indent=4)

        print("Successful archive.")

    """
        实例读档器
    """
    @classmethod
    def load(cls, world_type_name, file_name):
        """
            world_type_name:    world project的名字 格式同MTEAC类中的self.world_type_name
            file_name:          存档文件的名称 不需要加后缀 load方法会读取*file_name*.json文件 并生成一个相应的State实例
        """

        """
            使用字符串进行自动import
            此处要求world project中state.py和world.py中的类的命名规范:
                世界类型名： 名称_world
                世界类名要和世界类型名一致
                State名： 名称_state
            以及构造器中 属性名要和输入的参数名一致
            每个世界类型都应该有一个mods.py文件用于import world和state类
            如果不使用默认读档器则不需要在意这些规范
            （该逻辑待优化）
        """
        # 没有mods时使用 已经弃用
        # # 把 名称_world 转换为 名称_state
        # state_type_name_list = world_type_name.split("_")
        # state_type_name = '_'.join(state_type_name_list[:-1]) + "_state"
        # state_type_name = state_type_name.capitalize()
        #
        # # 通过名称_state读取状态类作为State
        # import importlib
        # # from world.world_project.mesh_world.state import Mesh_state as State
        # state_file = 'world.world_project.' + world_type_name + '.' + 'state'
        # generator_module = importlib.import_module(state_file)
        # State = getattr(generator_module, state_type_name)

        # 通过名称_state读取状态类作为State
        import importlib
        # from world.world_project.mesh_world.state import Mesh_state as State
        state_file = 'world.world_project.' + world_type_name + '.' + 'mods'
        generator_module = importlib.import_module(state_file)
        State = getattr(generator_module, "State")

        # 读取json字典的内容并结构化创建对象
        def json_to_state_obj(class_name, json_dict):
            if class_name == 'CDLL':
                return 0

            para_json = {}
            # 逐一取出属性名
            for para_name in json_dict:

                # if class_name == "State":
                #     print()

                # 判断属性值的类型
                if isinstance(json_dict[para_name], (int, str, float, bool)):
                    para_json[para_name] = json_dict[para_name]
                elif json_dict[para_name] is None:
                    para_json[para_name] = None
                # 若为数组 元组或字典
                elif isinstance(json_dict[para_name], list):
                    para_json[para_name] = list_json_read(json_dict[para_name])
                elif isinstance(json_dict[para_name], tuple):
                    para_json[para_name] = tuple_json_read(json_dict[para_name])
                elif isinstance(json_dict[para_name], dict):
                    para_json[para_name] = dict_json_read(json_dict[para_name])

            if class_name != "State" and class_name != "CDLL":
                Class_class = globals()[class_name]
            else:
                Class_class = State

            # if class_name == "State":
                # print()
            para_dict = {}

            for para in Class_class.__init__.__code__.co_varnames:
                if para in para_json:
                    para_dict[para] = para_json[para]

            # print(para_dict)
            # print(Class_class.__init__.__code__.co_varnames)

            instance = Class_class(**para_dict)

            return instance

        def list_json_read(json_list):
            tem_list = []
            for ele in json_list:
                if isinstance(ele, (int, str, float, bool)):
                    tem_list.append(ele)
                # None 处理
                elif ele is None:
                    tem_list.append(cls.list_json_ise(None))
                # 若为数组 元组或字典
                elif isinstance(ele, list):
                    tem_list.append(list_json_read(ele))
                elif isinstance(ele, tuple):
                    tem_list.append(tuple_json_read(ele))
                elif isinstance(ele, dict):
                    tem_list.append(dict_json_read(ele))

            return tem_list

        def tuple_json_read(json_tuple):
            return tuple(list_json_read(json_tuple))

        def dict_json_read(json_dic):
            goal_data = 0

            # 判断为普通词典还是对象词典还是function
            if "function" in json_dic:
                if json_dic["function"] == {}:
                    return 0
            # 对象字典的情况
            if len(json_dic) == 1 and \
                    isinstance([a for a in json_dic][0], str) and \
                    [a for a in json_dic][0][0].isupper():
                goal_data = \
                    json_to_state_obj([a for a in json_dic][0], json_dic[[a for a in json_dic][0]])
            # 普通字典的情况
            else:
                tem_dict = {}

                for key in json_dic:
                    # 元组字符串还原
                    key_type = key
                    if isinstance(key, str):
                        if '(' == key[0] and ')' == key[-1]:
                            key_type = tuple(key[1:-2].split(','))
                    if isinstance(json_dic[key], (int, str, float, bool)):
                        tem_dict[key_type] = json_dic[key]
                    elif json_dic[key] is None:
                        tem_dict[key_type] = None
                    # 若为数组 元组或字典
                    elif isinstance(json_dic[key], list):
                        tem_dict[key_type] = list_json_read(json_dic[key])
                    elif isinstance(json_dic[key], tuple):
                        tem_dict[key_type] = tuple_json_read(json_dic[key])
                    elif isinstance(json_dic[key], dict):
                        tem_dict[key_type] = dict_json_read(json_dic[key])
                goal_data = tem_dict
            return goal_data

        # 读取json存档文件内容
        path = os.getcwd()  # 获取当前路径
        with open(path + "\\" + "world\\world_project" + "\\" + world_type_name +
                  "\\save\\" + file_name + ".save", "r") as save_file:
            json_str = save_file.read()

        # json字符串转为字典
        json_dict = json.loads(json_str)
        # print(json_dict)

        # 根据字典结构化创建状态对象
        state = json_to_state_obj("State", json_dict)

        print("Successful load.")
        return state
