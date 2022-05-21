from world.entity.entity_import import *
from world.world_project.hexagonal_mesh_world.entity.creature.plant.birch_wood import Birch_wood
from world.world_project.hexagonal_mesh_world.entity.obj.human_corpse import Human_corpse
from world.world_project.hexagonal_mesh_world.entity.obj.axe import Axe

from world.world_project.hexagonal_mesh_world.entity.creature.animal.hexagonal_mesh_animal import Hexagonal_mesh_animal

"""
    人类类 物种类
    方法用于物种的行为的内部影响
"""


class Human_being(Hexagonal_mesh_animal, Human, Big_obj):
    # 物种属性
    feeding_habits = ["Fruit"]
    swimming_ability = 4
    life_area = "terrestrial"

    # 可以放进背包的物品
    pickable_objs = ["Fruit", "Stone", "Wood", "Axe", "Bucket"]

    # 合成表
    composed_table = {("Stone", "Wood"): ("Axe",),
                      ("Axe", "Wood", "Wood", "Wood"): ("Crafting_table",),
                      ("Axe", "Crafting_table", "Wood", "Wood", "Wood"): ("Axe", "Bucket", "Crafting_table"),
                      ("Axe", "Crafting_table", "Wood", "Wood", "Wood", "Wood", "Wood"):
                          ("Axe", "Cart", "Crafting_table"),
                      ("Axe", "Wood", "Wood", "Wood", "Stone", "Stone"): ("Axe", "Door"),
                      ("Axe", "Soil", "Soil", "Stone", "Stone", "Stone"): ("Axe", "Wall"),
                      }

    # 可以推拉的物品
    pushable = ["Cart"]

    # 可以收集的地貌 泥地 沙地 石头地
    collectable = [1, 2, 4]

    """
        行为合法性判断
    """
    action_list = ["go", "eat", "drink", "attack", "rest",
                   "pick_up", "put_down", "handling", "collect", "push",
                   "fabricate", "construct", "interaction", "use", ]

    def judge_go(self, world_state, command):
        direction = command[1]
        old_position = tuple(self.get_position())
        # 返回一格移动的位置 不考虑半格 可能为浮点或整数 浮点的化将在下面整数化 若出界则为False
        new_position = world_state.position_and_direction_get_adjacent(old_position, direction)

        # 地图边缘判断
        if new_position:
            # 若自己是半格则目的地也会是半格 置整
            new_position = (int(new_position[0]), int(new_position[1]))

            # 半格模式
            # 若在左右半格上
            if old_position[0] % 1 > 0:
                # 方向限制
                if direction == 'left' or direction == 'right':
                    return False
            # 若在上下半格上
            elif old_position[1] % 1 > 0:
                # 方向限制
                if direction == 'down' or direction == 'up':
                    return False

            # 整格模式
            # 攀爬限制 格差
            # 判断落差是否大于生物的爬行能力(水里不用看这个)
            if not "aquatic" and world_state.get_water_map()[new_position[0]][new_position[1]] < 1:
                if abs(world_state.landform_map[int(old_position[0])][int(old_position[1])] -
                       world_state.landform_map[int(new_position[0])][int(new_position[1])]) > \
                        self.get_crawl_ability():
                    return False

            # 地貌限制 水限制
            # 陆生动物下水限制
            if self.life_area == "terrestrial":
                if self.swimming_ability < world_state.get_water_map()[new_position[0]][new_position[1]]:
                    return False

            # 水生动物上岸限制
            if self.life_area == "aquatic":
                if world_state.get_water_map()[new_position[0]][new_position[1]] == 0:
                    return False

            # 实体限制 大物体限制
            if isinstance(self, Big_obj):
                # 大物体互斥规则
                # 如果有大动物挡在前面
                for other_entity in world_state.get_entities_in_position(new_position):
                    if isinstance(other_entity, Big_obj):
                        return False
                for other_entity in \
                        world_state.get_entities_in_position((
                                (old_position[0] + (new_position[0] - old_position[0]) / 2),
                                (old_position[1] + (new_position[1] - old_position[1]) / 2))
                        ):
                    if isinstance(other_entity, Big_obj):
                        return False

            # 挣扎状态判断
            if self.situation == "struggle":
                if random.randrange(100) <= 90:
                    return False

            return True
        else:
            return False

    def judge_eat(self, world_state, command):
        # 吃者
        eator = self
        # 吃的方向
        eat_direction = command[1]
        # 被吃着
        be_eator = command[2]

        # 没有对象
        if be_eator == -1:
            return False

        # 食性不合
        if not self.feeding_habits_judge(be_eator):
            return False

        if not isinstance(be_eator, Food):
            return False

        return True

    # 看喝的地方有没有水
    def judge_drink(self, world_state, command):
        direction = command[1]
        direction_position = world_state.position_and_direction_get_adjacent(self.get_position(), direction)
        if direction_position:
            return world_state.get_water_map()[int(direction_position[0])][int(direction_position[1])] > 0
        else:
            return False

    def judge_attack(self, world_state, command):
        be_attackeder = command[2]

        # 没有对象
        if be_attackeder == -1:
            return False

        if not isinstance(be_attackeder, Creature):
            return False

        return True

    def judge_rest(self, world_state, command):
        return True

    def judge_pick_up(self, world_state, command):
        # 被拾起之物
        be_pickor = command[2]

        # 没有对象
        if be_pickor == -1:
            return False

        # 判断可拾起性
        if be_pickor:
            if type(be_pickor).__name__ not in self.pickable_objs:
                return False

        return True

    def judge_put_down(self, world_state, command):
        # 放的方向
        direction = command[1]
        # 放的位置
        direction_position = world_state.position_and_direction_get_adjacent(self.get_position(), direction)

        if not direction_position:
            return False

        if command[2] == -1:
            return False

        return True

    def judge_handling(self, world_state, command):
        if command[2] == -1:
            return False

        if not isinstance(command[2], Equipment) and command[2] is not None:
            print("非装备不能装备")
            return False

        return True

    # command 为 [方法名， 空， 原材料]
    def judge_fabricate(self, world_state, command):
        if command[2] == -1:
            print("无对象")
            return False

        if not isinstance(command[2], (list, tuple)):
            print("原材料格式错误")
            return False

        if len(command[2]) == 0:
            print("原材料为空")
            return False

        names_orderly_tuple = names_orderly_tuplize(command[2])
        if names_orderly_tuple not in self.composed_table:
            print("原材料不合法")
            return False

        for outcome in self.composed_table[names_orderly_tuple]:
            if not outcome in self.pickable_objs:
                print("成品物品不可放入背包")
                return False

        return True

    # command 为 [方法名， 建造位置， 原材料]
    def judge_construct(self, world_state, command):
        if command[2] == -1:
            print("无对象")
            return False

        if not isinstance(command[2], (list, tuple)):
            print("原材料格式错误")
            return False

        if len(command[2]) == 0:
            print("原材料为空")
            return False

        if names_orderly_tuplize(command[2]) not in self.composed_table:
            print("原材料不合法")
            return False

        # 判断是否越界
        direction = command[1]
        direction_position = world_state.position_and_direction_get_adjacent(self.get_position(), direction)
        if direction_position:
            return True

        return False

    def judge_interaction(self, world_state, command):
        return False

    def judge_use(self, world_state, command):
        return False

    # command 结构类似于喝水
    # 看收集的地方能不能收集
    def judge_collect(self, world_state, command):
        # 得到收集处
        direction = command[1]
        direction_position = world_state.position_and_direction_get_adjacent(self.get_position(), direction)

        if direction_position:
            if tuple(direction_position) in world_state.get_plants_position():
                # 收集处是否有森林
                for plant in world_state.get_plants_position()[tuple(direction_position)]:
                    if isinstance(plant, Birch_wood):
                        return True

            # 收集处是否是可收集地貌
            return world_state.get_terrain_map()[int(direction_position[0])][int(direction_position[1])] in \
                   self.collectable
        else:
            return False

    """
        选择一个物体 选择一个方向 推/拉
        command = ["push", direction, obj]
        确保物体是可推拉的
        确保方向是合法的
            可go
            只能在直线方向上进行（不能并行）
        考虑半格的情况
            设计机制: 如果在半格上拉 则无反应（不在这里考虑）
    """
    def judge_push(self, world_state, command):
        # 得到方向和对象
        direction = command[1]
        obj = command[2]

        # 对象是否是可推的
        if type(obj).__name__ not in self.pushable:
            print("推拉对象不合法")
            return False

        # #
        # if not self.judge_go(world_state, ["go", direction]):
        #     print("推拉方向不合法")
        #     return False

        """
            通过判断运动后人和物的重合性判断是否物需要动
            如果人动 物不动 人物重合 说明是推 物需要动
            如果物动 人不动 人物重合 说明是拉 物需要动
            否则 物不需要动
            连判断方向都省了
        """

        # 判断移动是否是合法的
        if not self.judge_go(world_state, (0, direction)):
            print("人不能往这走")
            return False

        human_new_position = world_state.position_and_direction_get_new_position(self.get_position(), direction)
        if not human_new_position:
            print("人的推拉移动不合法")
            return False

        obj_new_position = world_state.position_and_direction_get_adjacent(obj.get_position(), direction)
        # 车不能被推到地图外
        if not obj_new_position:
            print("物不能推到地图外")
            return False

        if human_new_position == tuple(obj.get_position()) or obj_new_position == tuple(self.get_position()):
            return True

        # 推拉条件不对
        print("推拉条件不对")
        return False

    judge_action_method_list = [judge_go, judge_eat, judge_drink, judge_attack, judge_rest,
                                judge_pick_up, judge_put_down, judge_handling, judge_collect, judge_push,
                                judge_fabricate, judge_construct, judge_interaction, judge_use,
                                ]

    """
        行为内部结果执行
    """

    def go_outcome(self, parameter=None, obj=None, degree=None):
        # 这里parameter指的是移动到的新的位置 其它变量置None
        self.move(parameter)

    def eat_outcome(self, parameter=None, obj=None, degree=None):
        # 这里obj是被吃的对象
        self.full_value += 10
        # print(self.full_value)

    def drink_outcome(self, parameter=None, obj=None, degree=None):
        self.drinking_value += 10

    def attack_outcome(self, parameter=None, obj=None, degree=None):
        pass

    def rest_outcome(self, parameter=None, obj=None, degree=None):
        pass

    def pick_up_outcome(self, parameter=None, obj=None, degree=None):
        self.backpack.append(obj)

    def put_down_outcome(self, parameter=None, obj=None, degree=None):
        self.backpack.remove(obj)
        print("put down", obj)
        print(self.backpack)

    # 装备装备
    def handling_outcome(self, parameter=None, obj=None, degree=None):
        if self.equipment:
            self.equipment.cancel_gain(self)
            self.backpack.append(self.equipment)

        self.equipment = obj

        if obj:
            self.equipment.properties_gain(self)
            self.backpack.remove(self.equipment)

    # obj=消耗的材料
    def fabricate_outcome(self, parameter=None, obj=None, degree=None):
        costs = obj
        gains = self.composed_table[names_orderly_tuplize(costs)]

        # 失去原材料
        for item in costs:
            self.backpack.remove(item)

        for item_name in gains:
            item = globals()[item_name](self.get_position())
            self.backpack.append(item)

    def construct_outcome(self, parameter=None, obj=None, degree=None):
        costs = obj

        # 失去原材料
        for item in costs:
            if item in self.backpack:
                self.backpack.remove(item)

    def interaction_outcome(self, parameter=None, obj=None, degree=None):
        pass

    def use_outcome(self, parameter=None, obj=None, degree=None):
        pass

    # obj=所收集到的东西的数组
    def collect_outcome(self, parameter=None, obj=None, degree=None):
        gains = obj
        for item in gains:
            self.backpack.append(item)

    # parameter=方向, obj=推拉对象
    def push_outcome(self, parameter=None, obj=None, degree=None):
        # 这里parameter指的是移动到的新的位置 其它变量置None
        self.move(parameter)

    action_interior_outcome_method_list = [go_outcome, eat_outcome, drink_outcome, attack_outcome, rest_outcome,
                                           pick_up_outcome, put_down_outcome, handling_outcome,
                                           collect_outcome, push_outcome,

                                           fabricate_outcome, construct_outcome, interaction_outcome,
                                           use_outcome,
                                           ]

    """
        行为成本消耗
    """

    def go_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def eat_cost(self):
        pass

    def drink_cost(self):
        pass

    def attack_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def rest_cost(self):
        pass

    def pick_up_cost(self):
        pass

    def put_down_cost(self):
        pass

    def handling_cost(self):
        pass

    def fabricate_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def construct_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def interaction_cost(self):
        pass

    def use_cost(self):
        pass

    def collect_cost(self):
        self.body_change(full_value_change=-0.1, drinking_value_change=-0.1)

    def push_cost(self):
        self.body_change(full_value_change=-0.2, drinking_value_change=-0.2)

    action_cost_method_list = [go_cost, eat_cost, drink_cost, attack_cost, rest_cost,
                               pick_up_cost, put_down_cost, handling_cost, collect_cost, push_cost,
                               fabricate_cost, construct_cost, interaction_cost, use_cost,
                               ]

    def __init__(self, position, life, brain, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity, backpack=None):
        super(Human_being, self).__init__(position, life, brain, full_value, drinking_value, body_state,
                                          gender,
                                          crawl_ability, speed, aggressivity)
        self.backpack = backpack
        if not backpack:
            self.backpack = []
        self.equipment = None

    # 得到感知
    '''
        感知的结构： 整个是一个元组 其中：一个元组表示地形 另一个字典表示生物表
    '''

    def get_perception(self, landform_map, things_position):
        return tuple(landform_map), things_position

    def die(self):
        return [Human_corpse(self.get_position(), 20)]

    def get_backpack(self):
        return self.backpack[:]

    def move(self, new_position):
        self.position = new_position


def names_orderly_tuplize(objs_list):
    def get_onj_name(obj):
        return type(obj).__name__

    objs_name_list = [get_onj_name(obj) for obj in objs_list]
    objs_name_list.sort()
    return tuple(objs_name_list)
