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
            # State has the format [x_pos, y_pos, reward, moved, death, level, score, solved]
            state = self.thinIce_game.run('left')
            
            print(state)
            if state[3] == False:
                break
            

Agent().start_game()