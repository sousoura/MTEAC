"""
    动物是会运动 会行动的生物
"""

from world.entity.creature.creature import Creature
from world.entity.active_thing import Active_thing
from abc import ABCMeta, abstractmethod


class Animal(Creature, Active_thing, metaclass=ABCMeta):
    # 物种属性
    feeding_habits = []
    swimming_ability = 1
    life_area = 0

    def __init__(self, position, life, brain, health_point, full_value, drinking_value, body_state, gender,
                 crawl_ability, speed, aggressivity):
        super(Animal, self).__init__(position, life)

        """
            目前動物的屬性設計:
                基本属性
                    位置
                    大脑
                    
                合法行为集      类别          移动 攻击 吃 交配 喝水 休息
                    对应的行为影响方法
                
                状态属性
                    生命值          数值          float 0~100
                    饱腹值          数值          float 0~100
                    饮水值          数值          float 0~100
                    身体状态        数字 类别      健康 受伤 饥饿 缺水
                    
                属性属性（个体差异）
                    性别           布尔
                    
                能力属性
                    速度            数值           int
                    跃力            数值           int
                    攻击力          数值           int
                
                物种属性
                    食性            数组           能吃的物种的数量
                    大小（待修改）   布尔            True为女 False为男
                    水性            数值元组        能适应多深的水 在水里待多长时间 游泳速度等
                    生活场所         数字 类别       能不能上岸 能不能潜水：陆地生物 海洋生物 飞行生物 两栖生物
                    地貌兼容性（待修改）
                    飞行（待加）
                    
        """

        # 基本属性
        self.brain = brain

        # 状态属性
        self.health_point = health_point
        self.full_value = full_value
        self.drinking_value = drinking_value
        self.body_state = body_state

        # 个体属性
        self.gender = gender

        # 能力属性
        self.crawl_ability = crawl_ability
        self.speed = speed
        self.aggressivity = aggressivity

        self.geomorphic_compatibility = None

        # 行动状态属性
        """
            步距模式 每走一次的格数
                默认为一 随时可以在速度范围之内调
        """
        self.pace = 1

    @abstractmethod
    def move(self, new_position):
        pass

    @abstractmethod
    def get_perception(self, landform_map, things_position):
        pass

    # 想出一个行为
    def devise_an_act(self, perception):
        return self.brain.devise_an_act(perception, self)

    def get_speed(self):
        return self.speed

    def get_crawl_ability(self):
        return self.crawl_ability

    def judge_geomorphic_compatibility(self):
        return True

    # 判断行动合法性 属性对行动的影响体现在此
    # 判断行为是否因为动物内因的困难而无法进行
    def judge_action_legality(self):
        return True

    def change_pace(self, num):
        if isinstance(num, int):
            if 0 < num <= self.speed:
                self.pace = num

    def get_pace(self):
        return self.pace

    """
        待改进为用isinstance判断
    """
    @classmethod
    def feeding_habits_judge(cls, eat_object):
        return eat_object in cls.feeding_habits
