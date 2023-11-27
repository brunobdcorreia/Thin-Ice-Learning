from cmath import sqrt
import logging
import os
import random
from ThinIce import Game
import pickle as pkl
from queue import PriorityQueue
import math

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

    def h(self, tile1, tile2):
        return abs(tile1[0] - tile2[0]) + abs(tile1[1] - tile2[1])

    def next_states(self, tile):
        # print("tile:", tile)
        moves = self.map[tile]
        next_states = []

        for i in range(len(moves)):
            if moves[i] == 1:
                if i == 0:
                    next_states.append(((tile[0], tile[1] - 1), i))
                elif i == 1:
                    next_states.append(((tile[0] - 1, tile[1]), i))
                elif i == 2:
                    next_states.append(((tile[0], tile[1] + 1), i))
                elif i == 3:
                    next_states.append(((tile[0] + 1, tile[1]), i))

        return next_states

    def aStar(self, starting_level=1):
        m = self.thinIce_game.new(starting_level)
        self.load_map(starting_level)
        self.load_locations(starting_level)

        if self.map == {}:
            self.create_map(m)
            self.save_map(starting_level)
            self.save_locations(starting_level)

        # print("Map:")
        # for key, value in self.map.items():
        #     print(f'{key}: {value}')

        # print("Start:", self.start)
        # print("Goal:", self.goal)

        # Setando g() dos tiles
        g_score = {tile: float('inf') for tile in self.map}
        g_score[self.start] = 0

        # Setando f() dos tiles
        f_score = {tile: float('inf') for tile in self.map}
        f_score[self.start] = self.h(self.start, self.goal)

        # Printando os valores iniciais de g() e f()
        # print("g_score:")
        # for key, value in g_score.items():
        #     print(f'{key}: {value}')

        # Printando os valores iniciais de f()
        # print("f_score:")
        # for key, value in f_score.items():
        #     print(f'{key}: {value}')

        # Setando a fila de prioridade
        open_set = PriorityQueue()
        open_set.put((self.h(self.start, self.goal), self.h(self.start, self.goal), self.start))
        
        aPath = {}

        while not open_set.empty():
            current_tile = open_set.get()[2]
            if current_tile == self.goal:
                print("Goal reached!")
                break

            for i in range(4):
                if self.map[current_tile][i] == 1:
                    if i == 0:
                        neighbor = (current_tile[0], current_tile[1] - 1)
                    elif i == 1:
                        neighbor = (current_tile[0] - 1, current_tile[1])
                    elif i == 2:
                        neighbor = (current_tile[0], current_tile[1] + 1)
                    elif i == 3:
                        neighbor = (current_tile[0] + 1, current_tile[1])

                    temp_g_score = g_score[current_tile] + 1
                    temp_f_score = temp_g_score + self.h(neighbor, self.goal)

                    if temp_f_score < f_score[neighbor]:
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_f_score
                        open_set.put((temp_f_score, self.h(neighbor, self.goal), neighbor))
                        aPath[neighbor] = current_tile

        fwd_path = {}
        tile = self.goal
        while tile != self.start:
            fwd_path[aPath[tile]] = tile
            tile = aPath[tile]

        political_path = list(fwd_path.values())
        political_path.append(self.start)
        political_path.reverse()
        
        return political_path
    
    def convert_path(self, path):
        converted_path = []
        for i in range(len(path) - 1):
            if path[i][0] == path[i+1][0]:
                if path[i][1] > path[i+1][1]:
                    converted_path.append('up')
                else: converted_path.append('down')
            else:
                if path[i][0] > path[i+1][0]:
                    converted_path.append('left')
                else: converted_path.append('right')
        return converted_path

    def exploit(self, starting_level=1, path=[]):
        self.thinIce_game.new(starting_level)

        for action in self.convert_path(path):
            self.thinIce_game.run(action)

