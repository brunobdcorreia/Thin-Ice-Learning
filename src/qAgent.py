# Import ThinIce class from ThinIce.py
import random
import time
from ThinIce import *
import numpy as np
import os
import logging
import pickle as pkl
from Logger import Logger
from timeit import default_timer as timer
class QAgent:
    def __init__(self, learning_rate, algorithm, num_episodes, discount_factor):
        self.learning_rate = learning_rate
        self.algorithm = algorithm
        self.num_episodes = num_episodes
        self.discount_factor = discount_factor
        self.action = ['up', 'left', 'down', 'right']
        self.action_map = {'up': 0, 'left': 1, 'down': 2, 'right': 3}
        self.thinIce_game = Game()
        self.q_table = {}
        self.curr_state = []
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler('./q_table_debug.txt')
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    # def get_q_value(self, state, action):
    #     if state not in self.q_table:
    #         self.q_table[state] = np.zeros(len(self.action))
    #     return self.q_table[state][self.action.index(action)]        

    # Cria Q-table para o level atual. Lembrar de registrar o Q-table em um TXT
    def create_q_table(self, map: int) -> None:
        q_table_level = {}
        for i in range(len(map)):
            for j in range(len(map[i]) - 1):
                if (i != 0 and i != len(map)-1) and (map[i][j] != 'W' and map[i][j] != '0'):
                    # [up, left, down, right]
                    key = (j, i)
                    value = [0, 0, 0, 0]
                    q_table_level[key] = value
        self.q_table = q_table_level


    # Salva Q-table em um TXT
    def save_q_table(self, current_level: int) -> None:
        filename = f'data/behavior/any_percent/q_table{current_level}.pkl'
        with open(filename, 'wb') as f:
            pkl.dump(self.q_table, f)

    # Carrega Q-table de um TXT
    def load_q_table(self, current_level: int) -> None:
        filename = f'data/behavior/any_percent/q_table{current_level}.pkl'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.q_table = pkl.load(f)
        else:
            print(f'Arquivo {filename} não encontrado')

    def print_q_table(self):
        for key, value in self.q_table.items():
            self.logger.info(f'{key}: {value}')
                
    def update_q_table(self, curr_state, next_state, action):
        sample = self.get_sample(next_state)
        # print(f'Sample: {sample}')
        action_index = self.action_map[action]
        # print(f'Ação: {action}, index: {action_index}')
        # print(f'Q(s, a) antes de atualizar: {self.q_table[(curr_state[0], curr_state[1])][action_index]})')
        self.q_table[(curr_state[0], curr_state[1])][action_index] = (1 - self.learning_rate) * self.q_table[(curr_state[0], curr_state[1])][action_index] + self.learning_rate * sample
        # print(f'Q(s, a) depois de atualizar: {self.q_table[(curr_state[0], curr_state[1])][action_index]})')

    def get_sample(self, next_state):
        reward = None
        # Se o agente tentou ir em direção a parede, ou à água, recompensa é negativa
        if not next_state[2]:
            reward = -5
        # Se morreu, recompensa é negativa
        elif next_state[3]:
            reward = -5
        # Se completou a fase
        elif next_state[4]:
            reward = 1000
        # Punir por andar
        else: reward = -1

        # [i, j, up, left, down, right]
        sample = reward + self.discount_factor * max(self.q_table[(next_state[0], next_state[1])])
        return sample

    def explore(self, starting_level=1, xExploitation=0):
        m = self.thinIce_game.new(starting_level)

        self.load_q_table(starting_level)

        if self.q_table == {}:
            self.create_q_table(m)
            self.save_q_table(starting_level)
        
        # print("Q-Table:")
        # for key, value in self.q_table.items():
        #     print(f'{key}: {value}')

        self.curr_state = self.thinIce_game.run(self.action[random.randint(0, 3)])

        try:
            while True:         
                # [x_pos, y_pos, moved, death, solved, level]
                # Take random actions
                
                # print('Alterando estado...')
                if random.random() < xExploitation:
                    action_taken = np.argmax(self.q_table[(self.curr_state[0], self.curr_state[1])])
                else:
                    action_taken = self.action[random.randint(0, 3)]

                next_state = self.thinIce_game.run(action_taken)

                self.update_q_table(self.curr_state, next_state, action_taken)

                # print("Q-Table:")
                # for key, value in self.q_table.items():
                #     print(f'{key}: {value}')
                
                self.curr_state = next_state

                if self.curr_state[4] or self.curr_state[3]:
                    print("terminou de explorar!!!!")
                    self.save_q_table(starting_level)
                    # Clear self.q_table
                    self.q_table.clear()
                    break

        except Exception as e:
            print(e)
            self.logger.info(f'Erro: {e}')
            self.print_q_table()


    def exploit(self, starting_level=1, time_in_seconds=1):
        m = self.thinIce_game.new(starting_level)

        self.load_q_table(starting_level)

        if self.q_table == {}:
            return print('Q-table vazia. Execute o método explore() primeiro.')
        
        with open("data/q_states.csv", "a") as file:
            logger = Logger(1,file)
            for key, value in self.q_table.items():
                logger.log_csv(*key,*value, level=1)

        self.curr_state = self.thinIce_game.run(self.action[random.randint(0, 3)])

        total_reward = 0
        startTime = timer()
        logger = Logger(1)
        numPassos = 0;
        try:
            while True:         
                if (timer() - startTime > time_in_seconds):
                    break
                logger.log(f'S: {self.curr_state}', level=4)
                action_taken = np.argmax(self.q_table[(self.curr_state[0], self.curr_state[1])])
                total_reward += self.q_table[(self.curr_state[0], self.curr_state[1])][action_taken]
                action_taken = self.action[action_taken]
                logger.log(f'A: {action_taken}', level=4)

                next_state = self.thinIce_game.run(action_taken)
                logger.log(f'S\': {next_state}', level=4)

                self.curr_state = next_state
                numPassos+=1

                if self.curr_state[4] or self.curr_state[3]:
                    break
            with open("data/total_reward.csv", "a") as file:
                logger_cvs = Logger(1,file)
                logger_cvs.log_csv(total_reward, numPassos)
        
        except Exception as e:
            self.logger.info(f'Erro: {e}')
            self.print_q_table()
