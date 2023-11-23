# Import ThinIce class from ThinIce.py
import time
from ThinIce import *

g = TitleScreen()

# Vou ajustar umas coisas em ThinIce.py para que o agente possa executar comandos
# diretamente pelas classes, sem precisar manipular janela. Deve ficar mais fácil
# também de fazer o agente aprender a jogar, pois não vai precisar de uma janela
# e poderá acessar informações como a colisão com a parede, o gelo quebrado, etc.

while True:
    g.new()
    g.run()
    
    time.sleep(1)
    g.start()
    g.play()

    