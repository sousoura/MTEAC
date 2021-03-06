import os, sys

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
config_path = CURRENT_DIR.rsplit('\\', 2)[0]  # 上四级目录

# from_file = 'world/world_project/' + world_project_name + "/entity"

current_path = str(config_path).replace("\\" , "/") + "/world/entity"
current_py = "entity_import.py"

for root, dirs, files in os.walk(current_path):
    for name in files:
        if name[-3:] == ".py" and name != current_py:
            class_name = name[: name.rfind(".py")].capitalize()

            work_position = root[root.rfind("world/"):]
            path = os.path.join(work_position, name).replace("/", ".").\
                replace("..", ".").replace(".py", "").replace("\\", ".")

            import_string = "from " + path + " import " + class_name
            # print(import_string)
            exec(import_string)
