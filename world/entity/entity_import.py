import os

current_path = "world/entity"
current_py = "entity_import.py"

for root, dirs, files in os.walk(current_path):
    for name in files:
        if name[-3:] == ".py" and name != current_py:
            class_name = name[: name.rfind(".py")].capitalize()
            path = os.path.join(root, name).replace("/", ".").\
                replace("..", ".").replace(".py", "").replace("\\", ".")

            import_string = "from " + path + " import " + class_name
            # print(import_string)
            exec(import_string)
