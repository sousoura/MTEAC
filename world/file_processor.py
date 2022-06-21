import json
import os
from world.world_project.mesh_world.entity.mesh_entities import *
from world.entity.entity_import import *

"""
    file processor class
         Implemented default archive and load functions
         Function: load files and archives, all related to storage and reading are in this class
         (This logic is waiting to be improved)
"""


class File_processor:

    @classmethod
    def archive(cls, state, world_type_name, file_name):
        """
            state:              A state instance of a world project This instance holds all information about the current state of the worlds
            world_type_name:    The name of the world project, it has the same format as self.world_type_name in the MTEAC class
            file_name:          The name of the archive file, it does not need to be suffixed. After the archive is successful, the archive file will appear in the save folder of the world project
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
                # if it is an instance
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

        path = os.getcwd()  # Get the current path
        with open(path + "\\" + "world\\world_project" + "\\" + world_type_name +
                  "\\save\\" + file_name + ".save", "w+") as save_file:
            # json.dump(state, save_file, default=state_obj_to_json, sort_keys=True, indent=4)
            state_dic = state_obj_to_json(state)
            # print(state_dic)
            json.dump(state_dic, save_file, sort_keys=True, indent=4)

        print("Successful archive.")


    @classmethod
    def load(cls, world_type_name, file_name):
        """
            world_type_name:    The name of the world project, its format is the same as the self.World_type_name in the MTEAC class
            file_name:          The load function reads the file with the file_name and generates a corresponding State instance
                                It does not need to be suffixed
        """

        """
            import using string
            The naming conventions for classes in state.py and world.py in the world project are required here:
                name of World class：*name* + _world
                The world class name must be the same as the world type name
                name of State class： *name* + _state
            And the property name in the constructor should be the same as the input parameter name
            In each world project there should be a mods.py file for importing world and state classes
            You don't need to care about these specifications if you don't use the default file loader
            (This logic is waiting to be improved)
        """

        # UThe following code is used without mods.py and is deprecated

        # # find state_type_name
        # state_type_name_list = world_type_name.split("_")
        # state_type_name = '_'.join(state_type_name_list[:-1]) + "_state"
        # state_type_name = state_type_name.capitalize()
        #
        # # Read state class as State by state_type_name
        # import importlib
        # # from world.world_project.mesh_world.state import Mesh_state as State
        # state_file = 'world.world_project.' + world_type_name + '.' + 'state'
        # generator_module = importlib.import_module(state_file)
        # State = getattr(generator_module, state_type_name)

        # Read state class as State
        import importlib
        # from world.world_project.mesh_world.state import Mesh_state as State
        state_file = 'world.world_project.' + world_type_name + '.' + 'mods'
        generator_module = importlib.import_module(state_file)
        State = getattr(generator_module, "State")

        # Read the contents of the json dictionary and create objects structuredly
        def json_to_state_obj(class_name, json_dict):
            if class_name == 'CDLL':
                return 0

            para_json = {}
            # Extract property names one by one
            for para_name in json_dict:

                # if class_name == "State":
                #     print()

                # Determine the type of attribute value
                if isinstance(json_dict[para_name], (int, str, float, bool)):
                    para_json[para_name] = json_dict[para_name]
                elif json_dict[para_name] is None:
                    para_json[para_name] = None
                # If it is an array tuple or dictionary
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
                # deal with None
                elif ele is None:
                    tem_list.append(cls.list_json_ise(None))
                # If it is an array tuple or dictionary
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

            # Determine whether it is a normal dictionary or an object dictionary or a function
            if "function" in json_dic:
                if json_dic["function"] == {}:
                    return 0
            # The case of a dictionary representing an object
            if len(json_dic) == 1 and \
                    isinstance([a for a in json_dic][0], str) and \
                    [a for a in json_dic][0][0].isupper():
                goal_data = \
                    json_to_state_obj([a for a in json_dic][0], json_dic[[a for a in json_dic][0]])
            # For the case of a dictionary representing a normal dictionary
            else:
                tem_dict = {}

                for key in json_dic:
                    key_type = key
                    if isinstance(key, str):
                        if '(' == key[0] and ')' == key[-1]:
                            key_type = tuple(key[1:-2].split(','))
                    if isinstance(json_dic[key], (int, str, float, bool)):
                        tem_dict[key_type] = json_dic[key]
                    elif json_dic[key] is None:
                        tem_dict[key_type] = None
                    # If it is an array tuple or dictionary
                    elif isinstance(json_dic[key], list):
                        tem_dict[key_type] = list_json_read(json_dic[key])
                    elif isinstance(json_dic[key], tuple):
                        tem_dict[key_type] = tuple_json_read(json_dic[key])
                    elif isinstance(json_dic[key], dict):
                        tem_dict[key_type] = dict_json_read(json_dic[key])
                goal_data = tem_dict
            return goal_data

        # read json archive file content
        path = os.getcwd()  # get current path
        with open(path + "\\" + "world\\world_project" + "\\" + world_type_name +
                  "\\save\\" + file_name + ".save", "r") as save_file:
            json_str = save_file.read()

        # convert json string to dictionary
        json_dict = json.loads(json_str)
        # print(json_dict)

        # Create a state object based on a dictionary structure
        state = json_to_state_obj("State", json_dict)

        print("Successful load.")
        return state
