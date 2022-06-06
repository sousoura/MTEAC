from world_env_interface import WorldEnv
from gym.utils.env_checker import check_env

# program entry

if __name__ == "__main__":

    ai_mode = 1
    ai_num = 2

    env = WorldEnv()
    env.set_ai_num(ai_num)

    if ai_mode == 1:
        """
            openAI mode
        """
        while True:
            # Take a random action
            action = [env.action_space.sample() for num in range(ai_num)]
            obs, reward, done, info = env.step(action)

            if done[0] == 1:
                print("pac man win")
                break
            elif done[0] == -1:
                print("pac man lost")
                break

            # Render the game
            env.render("ai")

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
