# Trabalho IA - Gelo Fino por A* e Q-Learning

Este repositório contém os arquivos utilizados para o trabalho final do curso de Inteligência Artificial da Universidade Federal da Bahia. Foram desenvolvidos dois agentes, um por A* e outro por Q-Learning, que aprenderam a jogar o minigame Gelo Fino, originalmente do MMO Club Penguin, e performar uma partida no menor tempo possível.
## Introdução

Club Penguin se tratava de um jogo massivo online (MMO), onde jogadores poderiam interagir entre si e se envolver em diversos eventos e jogos do mundo virtual.

Em fevereiro de 2017, foi anunciado que os servidores dos popular jogo online Club Penguin seriam desligados. Logo em seguida, a comunidade de jogadores se mobilizou para preservar o jogo e seus minigames criando cópias públicas dos softwares.

Um dos jogos do Club Penguin que recebeu bastante destaque pela comunidade foi Gelo Fino, um minigame cujo objetivo era controlar um personagem, o Puffle, de um ponto inicial até o destino, andando sobre casas de gelo que derretem a cada movimento do jogador.

Além do esforço pela preservação do jogo, em torno de Gelo Fino se contruiu uma comunidade de jogadores que competiam entre si para disputar quem completava o jogo no menor tempo possível. A essa modalidade de competição, que está presente em diversos outros jogos, se atribui o termo Speed Run. No caso de uma corrida (run) em menor tempo possível, sem outras condições, se atribui o termo Any\%.

Esse trabalho tem como objetivo desenvolver dois agentes de inteligência artifical que, para um dada fase de Gelo Fino, forneça não apenas o caminho ótimo mas também sirva como referência para o menor tempo possível de uma run Any\%.

Para isso, utilizando uma versão em python de Gelo Fino modificada, dois agentes que aprendem sobre as fases e iteram sobre o jogo foram construídos, um pelo algoritmo A* e o outro por Q-Learning.
## Algoritmos

Para a construção dos agentes que iterariam sobre o jogo e obteriam o menor caminho para cada fase, optamos por adotar a implementação dos algoritmos A* (A-star) e Q-Learning. Para cada abordagem, uma classe de agente distinta foi desenvolvida a fim de manter maior consistência dos métodos que envolvem cada implementação.

### A-star

Conhecido por ser implementado em contextos de busca por menor caminho entre dois pontos em um conjunto matricial, a escolha de A* foi uma decisão quase imediata dada a natureza do jogo Gelo Fino.

Uma vez tendo acesso ao mapeamento dos estados e os possível próximos estados a partir deste, bastou implementar o algoritmo tradicional de A* para a construção do agente. O algoritmo retornaria o caminho ótimo do início ao fim do mapa, cabendo então ao agente performar as referidas ações.

Sobre cada nível, o agente pôde encontrar o caminho ótimo do ponto inicial ao final. Esse trajeto foi armazenado em uma lista de ações, cujas instruções armazenadas seriam do tipo 'up', 'left', 'right' e 'down'. Essa lista foi armazenada em um arquivo cujo acesso poderia ser feito no momento que o agente exploitaria o mapa.

No momento do exploit, bastou acessar e passar ao jogo a lista de ações obtida para que o Puffle percorresse o nível no menor tempo possível.

### Q-Learning

Em contraste ao A*, o Q-Learning surgiu como alternativa por sua versatilidade e potencial em conseguir solucionar outros problemas, como encontrar o caminho ótimo para uma full run, onde o Puffle percorreria todos os blocos a fim de maximizar a sua pontuação.

Além de acessar todos os possíveis estados em uma fase, a classe do agente por Q-Learning precisava manter registro de todos os Q-Values para um dado estado. Para isso, foi criada e armazenada uma Q-Table para cada fase, que mapeava para um dado estado, sinalizado por suas coordenadas, os valores para ações cima, esquerda, baixo e direita.

Para a exploração, o agente iniciaria uma partida em um dado nível tomando ações aleatórias e mantendo o registro dos Q-Values para os correspondentes Q-States para a dada ação tomada.

Nós decidimos por utilizar a taxa de aprendizado e fator de desconto como varáveis de controle para observar o comportamento do Q-learning e descutiremos os resultados nessa sessão. Foram feitos 200 episódios variando taxa de aprendizado em $0.2,0.5,0.8$ e fator de desconto em $0.5,0.8,0.99$ na fase 8 do jogo. No total, foram $9*200$ episódios que serão entregues anexo à atividade. A função de recompensa, por sua vez, foi construída visando punir o agente por morrer (-5), andar contra a parede ou água (-5) e por andar (-1), sendo recompensado ao concluir a fase (+1000).

Para o exploit de um certo nível, bastou o agente acessar a Q-Table correspondente e iterá-la buscando a melhor ação de um dado estado, informando a ação ao jogo, e buscando a próxima melhor ação do estado seguinte. O Puffle, após vários episódios de exploração, conseguiu encontrar percorrer todos os níveis explorados no menor tempo possível.
## Execução

Ambos os agentes desenvolvidos se encontram em seus respectivos arquivos, aStarAgent.py e qAgent.py. Um código main.py foi desenvolvido para facilitar a manipulação das operações e execução dos códigos.

No diretório /src, basta executar o comando py main.py com algumas das seguintes flags:

'--learning-rate', type=float, default=0.75: Taxa de aprendizado do agente
'--algorithm', type=str, default='q-learning': Algoritmo a ser executado. Pode ser A-star ou Q-learning
'--num-episodes', type=int, default=10: Número de episódios para treinamento
'--discount-factor', type=float, default=0.99: Fator de desconto do agente.
'--starting-level', type=int, default=1: Nível inicial do jogo.
'--exploit', type=bool, default=False: Se o agente vai exploitar ou não
'--metricas', type=bool, default=False: Faz um episódio e registra a recompensa
'--explore', type=bool, default=False: Se o agente vai explorar ou não
'--full-run', type=bool, default=False: Se o agente vai exploitar todos os mapas

Abaixo listamos exemplos de algumas execuções comuns.

Para executar o explore de q-learning sobre a fase 1 em 5 episódios:
py main.py --algorithm=q-learning --explore=True --starting-level=1 --num-episodes=5

Para executar o exploit de q-learning sobre a fase 1:
py main.py --algorithm=q-learning --exploit=True --starting-level=1

Para executar o exploit de q-learning sobre todas as fases:
py main.py --algorithm=q-learning --full-run=True

Para executar o exploit de a-star sobre a fase 1:
py main.py --algorithm=a-star --exploit=True --starting-level=1

Para executar o exploit de q-learning sobre todas as fases:
py main.py --algorithm=a-star --full-run=True
