from world_env_interface import WorldEnv
from gym.utils.env_checker import check_env

# program entry

if __name__ == "__main__":

    """
        ai_mode为1：以openAI gym的模式运行
        ai_mode为2：以游戏模式运行 只有当world project支持game mode时才能运行 具体参见使用说明文档
            游戏模式和ai模式的区别在于环境中的实体在游戏模式中由玩家而不是ai操控
        ai_mode为3：检查WorldEnv是否符合openAI gym的要求 测试环境是否能跑通
    """
    ai_mode = 2

    """
        定义有几个 agent
            该变量决定了action数组的长度
            （该逻辑待改进）
    """
    ai_num = 1

    env = WorldEnv()
    env.set_ai_num(ai_num)

    if ai_mode == 1:
        """
            openAI mode
        """
        while True:
            # Take random actions
            action = [env.action_space.sample() for num in range(ai_num)]

            # 执行动作 并得到结果
            obs, reward, done, info = env.step(action)

            # 吃豆人胜利和失败判断
            if done[0] == 1:
                print("pac man win")
                break
            elif done[0] == -1:
                print("pac man lost")
                break

            # Render the game
            env.render("ai")

            # 如果游戏结束 则退出游戏
            if done is True:
                break

        # 关闭gym的环境
        env.close()
    elif ai_mode == 2:
        """
            游戏模式
        """
        env.game_mode()

    elif ai_mode == 3:
        check_env(env)
