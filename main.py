from world_env_interface import WorldEnv
from gym.utils.env_checker import check_env

# 程序入口

if __name__ == "__main__":
    ai_mode = 1
    env = WorldEnv()

    if ai_mode == 1:
        """
            openAI模式
        """
        while True:
            # Take a random action
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            obs = env.reset()

            # Render the game
            env.render()

            if done is True:
                break

        env.close()
    elif ai_mode == 2:
        """
            普通模式
        """
        env.game_mode()

    elif ai_mode == 3:
        check_env(env)
