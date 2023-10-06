import pygame

game_state = {}

class GameState():
    def __init__(self, name, screen, background=None):
        self.name = name
        if background:
            self.background = background
        self.screen = screen
        game_state[name] = False

    def draw(self):
        pass

    def enable(self):
        global game_state
        game_state = {key: False if key != self.name else True for key in game_state}

    def is_enabled(self):
        if game_state[self.name]:
            return True
        else:
            return False
