import importlib
import threading

import gym
import random
import numpy as np
from gym import Env, spaces

if __name__ == "__main__":
    from world.file_processor import File_processor
else:
    import sys, os
    sys.path.append(os.path.dirname(__file__))

    from world.file_processor import File_processor

"""
    The class representing MTEAC
        Both as an environment class that meets the requirements of openAI and as a manager for managing world projects.
"""


# 控制整个程序的进程
class WorldEnv(Env):
    """
        The main functions of this class are:
            initialization method
            functions required by openAI gym
                step()
                reset()
                render()
                etc...
            game_mode() function
            save(), load() function

        initialization
            choose world project
            choose between generating a world or reading a file
            During initialization, a World instance will be generated to run as a world project

        If the world project supports the background, the background will be enabled
            the program is divided into two threads
                main program thread
                Background command thread (this thread will use the input() method to read in background commands)
            Currently only mesh_world supports backend
            (This logic is waiting to be improved)
    """

    """
            ======================
                   initialization function
            ======================
    """
    def __init__(self):
        """
            Select here which world project MTEAC points to
        """
        # self.world_type_name = input("Please input world type name: ")
        # self.world_type_name = "blank_world"
        # self.world_type_name = "block_world"
        self.world_type_name = "mesh_world"
        # self.world_type_name = "round_the_clock_world"
        # self.world_type_name = "eight_direction_mesh_world"
        # self.world_type_name = "hexagonal_mesh_world"
        # self.world_type_name = "physics_world"
        # self.world_type_name = "pac_man_world"

        self.generator = None

        print("start creating the world")
        self.world = self.world_create()
        print("world creation is complete")

        if self.world:
            """
                Exhibitor is responsible for the visual presentation of the window
                Every world project must have an Exhibitor class, even if it is empty
            """
            # 创建可视化窗口 后面那个数是世界的格子大小
            print("Start creating visualizations")
            exhibitor_file = 'world.world_project.' + self.world_type_name + '.' + 'exhibitor'
            exhibitor_module = importlib.import_module(exhibitor_file)
            """
                The value and purpose of the second parameter is determined by the logic in the Exhibitor class in the specific world project.
            """
            self.exhibitor = exhibitor_module.Exhibitor(self.world, 15)
            print("visualization instance creation is complete")

        """
            The seed() function is not implemented yet
            it is waiting to be improved
        """
        self.seed()

        self.action_space, self.observation_space = self.world.get_openai_action_space_and_observation_space()
        self.ai_num = 1

    # 程序入口
    """
        This part is responsible for the user's initial selection
        The user chooses which world to enter, generate or read
        Generate and return a world instance based on user input
        
        This feature can be improved on the front end
    """

    def world_create(self):
        # Get the corresponding world generator through world type name
        def get_generator(generator_file):
            generator_file = 'world.world_project.' + generator_file + '.' + 'world_generator'

            try:
                generator_module = importlib.import_module(generator_file)

            except ModuleNotFoundError:
                # can not find this type of world
                return None

            return generator_module.Concrete_world_generator()

        """
           Choose whether to generate a new world or read an existing archive
        """
        # entry_mode = "load"
        entry_mode = "generate"

        # Get world generator based on world type
        self.generator = get_generator(self.world_type_name)

        world = None
        # generate a new world
        if entry_mode == "generate":
            # Generate a world with the world generator
            world = self.generator.default_generate_a_world()

        # load a world
        elif entry_mode == "load":
            world_name = input("Please input world name: ")
            while world is None:
                try:
                    # Read a world through the loader
                    world = self.load(self.world_type_name, world_name)
                except FileNotFoundError:
                    world = None
                    world_name = input("Can't find this file, Please correct input and input world name again: ")

        return world

    """
        ======================
            functions of openAI gym
        ======================
    """
    def step(self, action):
        obs = []
        reward = []
        done = []
        info = []

        for ai_id in range(1, self.ai_num + 1):
            rwd, dn = self.world.take_action\
                (self.world.translate_openai_command_to_mteac(self.world.state, action[ai_id - 1]), ai_id)
            obs.append(self.world.translate_mteac_state_to_openai(self.world.state))
            reward.append(rwd)
            done.append(dn)
            info.append(None)

        is_done = self.world.evolution()
        if is_done:
            done = is_done

        return obs, reward, done, info

    """
        This method is called every turn the world runs. Statistics and visualizations happen here
    """

    def render(self, mode="ai"):
        def visualization():
            return self.exhibitor.display(mode)

        return visualization()

    def reset(self):
        return self.world.translate_mteac_state_to_openai(self.world.state)

    def seed(self, seed=None):
        pass

    def close(self):
        pass

    def set_ai_num(self, ai_num):
        self.ai_num = ai_num

    """
        ======================
            functions of game mode
        ======================
        Currently only valid for mesh_world
        The class variable play_mode defines whether game_mode is available
    """
    def game_mode(self):
        """
            An endless loop that keeps the world running until the background asks to quit or the program is closed
        """
        def world_evolution():
            """
                In mesh_world:
                    under "normal" mode, the world will wait for player input before it will work
                    under "no_waiting" mode, the world works even without player input
            """
            # mode = "no_waiting"
            mode = "normal"

            self.player_cmd = self.render(mode)
            # print("The player command is: ", self.player_cmd)
            # Use variable self.gate to determine whether to end
            while self.gate:
                # print("The world runs once")
                self.world.take_action(self.player_cmd, 1)
                self.world.evolution()
                # print("Run once complete")
                # subsequent operations: visualization, etc.
                self.player_cmd = self.render(mode)
                # print("The player command is: ", self.player_cmd)
                if not self.player_cmd:
                    self.gate = False

        """
            Terminal background, users can input commands to control the program
                Currently only mesh_world and its cousin world_project support this function
                Currently supported commands are：
                    quit: exit the program
                    save *name of save file*: Save the current world to the archive name.save file
        """
        def background():
            if self.world.backgroundable:
                while self.gate:
                    background_cmd = input("Please input command: \n")

                    cmd = background_cmd.split(' ')
                    if cmd[0] == "quit":
                        self.gate = False
                        self.exhibitor.set_out()
                        break
                    elif cmd[0] == "save":
                        if len(cmd) == 1:
                            cmd.append('save')
                        self.save(cmd[1])
                    elif cmd[0] == "stat":
                        if self.world.statistical:
                            try:
                                print(self.world.statistics(cmd))
                            except ValueError:
                                print("The parameter format is incorrect, please check the parameters and input again")
                        else:
                            print("The program is not statistical.")
                    else:
                        print("wrong command,please check and input again")
            else:
                print("The world has no background function.")

        """
            the world works in game mode
        """
        # If the world is successfully generated, enter the world, otherwise exit the program
        if self.world:
            if self.world.play_mode:
                print("The world is created successfully")
                # Initialize the thread and run the gate, the background thread and the main thread are synchronized
                self.background_thread = threading.Thread(target=background)
                # Initiate user action variable
                self.player_cmd = 1
                self.gate = True

                """
                    Create background thread
                """
                # Backstage and the world started to work non-stop
                self.background_thread.setDaemon(True)
                print("Create backend")
                self.background_thread.start()
                print("The world starts to work")
                world_evolution()
            else:
                print("This world project does not support player mode")
        else:
            print("world creation failed")

    """
        ======================
            Archiving and loading functions
        ======================
    """
    """
        archiving function
        When the player calls and specifies the save name, the File_processor object will be called to save the current world in the save folder in json format.
        The specific function is implemented by the File_processor object
        
        Background archive command format: save archive name
    """
    def save(self, file_name):
        print("archiving...")
        world_type_name = type(self.world).__name__
        state = self.world.get_state()
        File_processor.archive(state, world_type_name, file_name)

    """
        loading function
        The specific function is implemented by the File_processor object
        parameters:
             world_type_name world type
             file_name Archive name
        returns a world object
    """
    def load(self, world_type_name, file_name):
        print("loading...")
        state = File_processor.load(world_type_name, file_name)
        world = self.generator.generate_a_world_by_state(state)
        return world
