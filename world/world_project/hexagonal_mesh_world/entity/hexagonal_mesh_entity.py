"""
    物种自动引入器
"""

import os

world_project_name = "hexagonal_mesh_world"

current_path = "world/world_project/" + world_project_name + "/entity"
current_py = "hexagonal_mesh_entity.py"

for root, dirs, files in os.walk(current_path):
    for name in files:
        if name[-3:] == ".py" and name != current_py:
            class_name = name[: name.rfind(".py")].capitalize()
            path = os.path.join(root, name).replace("/", ".").\
                replace("..", ".").replace(".py", "").replace("\\", ".")

            import_string = "from " + path + " import " + class_name
            # print(import_string)
            exec(import_string)
