from world.exhibitor_super import Exhibitor_super


class Exhibitor(Exhibitor_super):
    def __init__(self, world, size_para):
        self.world = world
        self.size_para = size_para

    def display(self, mode):
        for line in self.world.state.game_map:
            print(line)
        print()

        print("pac man position:", self.world.state.pac_man.get_position())

        for ghost in self.world.state.ghosts:
            print("ghost position:", ghost.get_position())

        print("beans position: ", end="")
        for bean in self.world.state.beans:
            print(bean.get_position(), end=' ')

        print()

    def set_out(self):
        pass
