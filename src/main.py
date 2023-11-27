import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import importlib.util
import argparse
from qAgent import QAgent
from aStarAgent import AStarAgent

def module_is_installed(module_name: str) -> bool:
    spec = importlib.util.find_spec(module_name)
    
    if spec is None:
        print(f'Módulo {module_name} não encontrado.')
        return False
    else: return True

def install_dependencies(dependency_file_path: str):
    with open(dependency_file_path, 'r', encoding='utf-16') as file:
        modules = file.readlines()

        for module in modules:
            module = module.strip().split("=")[0]
            print(f'Checando se {module} está instalado...')
            if module_is_installed(module): pass
            else: 
                print(f'Instalando {module}...') 
                os.system(f'pip install {module}')

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Trabalho de IA')
    parser.add_argument('--dependency-file-path', type=str, default='../requirements.txt', help='Caminho para o arquivo de dependências')
    parser.add_argument('--learning-rate', type=float, default=0.75, help='Taxa de aprendizado do agente')
    parser.add_argument('--algorithm', type=str, default='q-learning', help='Algoritmo a ser executado. Pode ser A-star ou Q-learning')
    parser.add_argument('--num-episodes', type=int, default=10, help='Número de episódios para treinamento')
    parser.add_argument('--discount-factor', type=float, default=0.99, help='Fator de desconto do agente.')
    parser.add_argument('--starting-level', type=int, default=1, help='Nível inicial do jogo.')
    parser.add_argument('--exploit', type=bool, default=False, help='Se o agente vai exploitar ou não')
    parser.add_argument('--metricas', type=bool, default=False, help='Faz um episódio e recorda a recompensa')
    parser.add_argument('--explore', type=bool, default=False, help='Se o agente vai explorar ou não')
    parser.add_argument('--full-run', type=bool, default=False, help='Se o agente vai exploitar todos os mapas')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_cmd_arguments()

    # # Q-learning
    if args.algorithm == 'q-learning':
        game_agent = QAgent(learning_rate=args.learning_rate, algorithm=args.algorithm, num_episodes=args.num_episodes, discount_factor=args.discount_factor)

        if args.exploit:
            game_agent.exploit(args.starting_level, args.metricas)
        elif args.explore:
            for i in range(args.num_episodes):
                print(f'Episódio {i+1}')
                game_agent.explore(args.starting_level, args.metricas)
        elif args.full_run:
            for i in range(1, 10):
                print(f'Episódio {i}')
                game_agent.exploit(i, args.metricas)
        elif args.metricas:
            for i in range(1, args.num_episodes):
                print(f'Episódio {i}')
                game_agent.explore(args.starting_level, args.metricas)
                game_agent.exploit(args.starting_level, args.metricas)

        else:
            print('Nenhuma opção selecionada. Por favor, selecione --exploit ou --explore')

    elif args.algorithm == 'a-star': 
        # A-star
        game_agent = AStarAgent()
        if args.exploit:    
            path = game_agent.aStar(args.starting_level)
            game_agent.exploit(args.starting_level, path)
        elif args.full_run:
            for i in range(1, 10):
                print(f'Episódio {i}')
                path = game_agent.aStar(i)
                game_agent.exploit(i, path)

    else: print('Algoritmo inválido. Por favor, selecione A-star ou Q-learning')