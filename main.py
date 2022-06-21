from world_env_interface import WorldEnv
from gym.utils.env_checker import check_env

# program entry

if __name__ == "__main__":

    """
        when ai_mode is 1：Run in openAI gym mode
        when ai_mode is 2：Run in game mode. It can only run when the world project supports game mode. 
                           For details, please refer to the user manual.
            The difference between game mode and ai mode is that the entities in the environment are controlled by the player instead of the ai in game mode.
        ai_mode为3：Check whether WorldEnv meets the requirements of openAI gym and whether the test environment can run through
    """
    ai_mode = 1

    """
        Define how many agents there are
            This variable determines the length of the action array
            (This logic is waiting to be improved)
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

            # perform the action and get the result
            obs, reward, done, info = env.step(action)

            # # Pac-Man victory and defeat judgment
            # if done[0] == 1:
            #     print("pac man win")
            #     break
            # elif done[0] == -1:
            #     print("pac man lost")
            #     break

            # Render the game
            env.render("ai")

            # If the game is over then exit the game
            if done is True:
                break

        # Close the gym's environment
        env.close()
    elif ai_mode == 2:
        """
            game mode
        """
        env.game_mode()

    elif ai_mode == 3:
        check_env(env)
