import logging
import os
from ThinIce import Game
import pickle as pkl
from queue import PriorityQueue

class AStarAgent:
    def __init__(self):
        self.action = ['up', 'left', 'down', 'right']
        self.action_map = {'up': 0, 'left': 1, 'down': 2, 'right': 3}
        self.thinIce_game = Game()
        self.map = {}
        self.start = ()
        self.goal = ()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler('./map_debug.txt')
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def load_map(self, current_level: int) -> None:
        filename = f'data/behavior/any_percent/a-star_map{current_level}.pkl'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.map = pkl.load(f)
        else:
            print(f'Arquivo {filename} não encontrado')

    def load_locations(self, current_level: int) -> None:
        filename = f'data/behavior/any_percent/a-star_locations{current_level}.pkl'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.start, self.goal = pkl.load(f)
        else:
            print(f'Arquivo {filename} não encontrado')

    def create_map(self, map: int) -> None:
        map_level = {}
        for i in range(len(map)):
            for j in range(len(map[i]) - 1):
                if (i != 0 and i != len(map)-1) and (map[i][j] != 'W' and map[i][j] != '0'):
                    # [up, left, down, right]
                    key = (j, i)
                    
                    value = [map[i-1][j], map[i][j-1], map[i+1][j], map[i][j+1]]
                    value = [1 if x != 'W' and x != '0' else 0 for x in value]

                    map_level[key] = value

                    if map[i][j] == 'P':
                        self.start = key
                    elif map[i][j] == 'E':
                        self.goal = key
                    
        self.map = map_level

    def save_map(self, current_level: int) -> None:
        filename = f'data/behavior/any_percent/a-star_map{current_level}.pkl'
        with open(filename, 'wb') as f:
            pkl.dump(self.map, f)

    def save_locations(self, current_level: int) -> None:
        filename = f'data/behavior/any_percent/a-star_locations{current_level}.pkl'
        with open(filename, 'wb') as f:
            pkl.dump((self.start, self.goal), f)

    def print_map(self):
        for key, value in self.map.items():
            self.logger.info(f'{key}: {value}')

    def h(self, tile):
        return abs(tile[0] - self.goal[0]) + abs(tile[1] - self.goal[1])

    def next_states(self, tile):
        moves = self.map[tile]
        next_states = []

        for i in range(len(moves)):
            if moves[i] == 1:
                if i == 0:
                    next_states.append((tile[0], tile[1] - 1))
                elif i == 1:
                    next_states.append((tile[0] - 1, tile[1]))
                elif i == 2:
                    next_states.append((tile[0], tile[1] + 1))
                elif i == 3:
                    next_states.append((tile[0] + 1, tile[1]))

        return next_states

    def aStar(self, starting_level=1):
        m = self.thinIce_game.new(starting_level)
        self.load_map(starting_level)
        self.load_locations(starting_level)

        if self.map == {}:
            self.create_map(m)
            self.save_map(starting_level)
            self.save_locations(starting_level)

        print("Map:")
        for key, value in self.map.items():
            print(f'{key}: {value}')

        print("Start:", self.start)
        print("Goal:", self.goal)

        # Setando g() dos tiles
        g_score = {tile: float('inf') for tile in self.map}
        g_score[self.start] = 0

        # Setando f() dos tiles
        f_score = {tile: float('inf') for tile in self.map}
        f_score[self.start] = self.h(self.start)

        # Printando os valores iniciais de g() e f()
        print("g_score:")
        for key, value in g_score.items():
            print(f'{key}: {value}')

        # Printando os valores iniciais de f()
        print("f_score:")
        for key, value in f_score.items():
            print(f'{key}: {value}')

        # Setando a fila de prioridade
        open_set = PriorityQueue()
        open_set.put((self.start, f_score[self.start]))
        
        print("open_set:\n[(x, y), f_score]")
        for i in open_set.queue:
            print(i)


