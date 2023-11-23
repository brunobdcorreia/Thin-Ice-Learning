# Import ThinIce class from ThinIce.py
import time
from ThinIce import *

class Agent:
    def __init__(self):
        self.action = ''
        self.thinIce_game = Game()
        self.against_wall = False

    def start_game(self):
        self.thinIce_game.new()

        while True:
            if not self.against_wall:
                self.action = 'left'
            else:
                self.action = 'right'
            self.thinIce_game.agent_run(self)
            

Agent().start_game()

    