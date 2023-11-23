import importlib.util
import os
import argparse

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
    parser.add_argument('--roms-directory-path', type=str, default='../autorom', help='Caminho para o diretório de ROMs')
    parser.add_argument('--game', type=str, default='LostLuggage-v5', help='Nome do jogo a ser executado')
    parser.add_argument('--render-mode', type=str, default='human', help='Modo de renderização')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_cmd_arguments()
    install_dependencies(args.dependency_file_path)
    
    import gymnasium as gym
    import shimmy
    import ale_py

    env = gym.make(f'ALE/{args.game}', render_mode=args.render_mode)
    env.metadata['render_fps'] = 60
    env.reset()
    for _ in range(1000):
        env.render()
        env.step(env.action_space.sample())
    env.close()