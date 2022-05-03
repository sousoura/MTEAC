"""
    动物是会运动 会行动的生物
"""

from world.entity.creature.creature import Creature
from world.entity.active_thing import Active_thing
from abc import ABCMeta, abstractmethod


class Animal(Creature, Active_thing, metaclass=ABCMeta):

    def __init__(self, position, life, brain):
        super(Animal, self).__init__(position, life)

        """
            目前動物的屬性設計:
                合法行为集      类别          移动 攻击 吃 交配 喝水 休息
                    对应的行为影响方法
                
                状态属性
                    生命值          数值          float 0~100
                    饱腹值          数值          float 0~100
                    饮水值          数值          float 0~100
                    身体状态        类别          健康 受伤 饥饿 缺水
                    
                属性属性
                    性别
                    
                能力属性
                
                物种属性
                    食性
                    
        """
        self.brain = brain
        self.crawl_ability = 1
        self.speed = 1
        self.geomorphic_compatibility = None

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
