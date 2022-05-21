"""
    物种自动引入器
"""

import os, sys

world_project_name = "hexagonal_mesh_world"
current_py = "hexagonal_mesh_entity.py"

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
config_path = CURRENT_DIR.rsplit('\\', 4)[0]  # 上四级目录

current_path = str(config_path).replace("\\" , "/") + '/world/world_project/' + world_project_name + "/entity"


for root, dirs, files in os.walk(current_path):
    for name in files:
        if name[-3:] == ".py" and name != current_py:
            class_name = name[: name.rfind(".py")].capitalize()

            work_position = root[root.rfind("world/world_project"):]
            path = os.path.join(work_position, name).replace("/", ".").\
                replace("..", ".").replace(".py", "").replace("\\", ".")

            import_string = "from " + path + " import " + class_name
            # print(import_string)

            exec(import_string)
