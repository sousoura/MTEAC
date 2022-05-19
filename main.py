from world_env_interface import WorldEnv

# 程序入口

if __name__ == "__main__":
    ai_mode = True
    if ai_mode:
        """
            openAI模式
        """
        env = WorldEnv()

        while True:
            # Take a random action
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            env.reset()

            # Render the game
            env.render()

            if done is True:
                break

        env.close()
    else:
        """
            普通模式
        """
        a = WorldEnv()
        a.test()
