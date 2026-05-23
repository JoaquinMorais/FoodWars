from classes.game import Game
from classes.action import ActionType
from classes.races.predator import Predator

"""ind = Predator()
print(ind.eat())
print(ind.can_eat())
print(ind.days_without_eating)"""

from classes.races.neural import Neural


game = Game()

import os
from classes.races.neural import NeuralBrain
if os.path.exists("mejor_cerebro.json"):
    cerebro = NeuralBrain.cargar("mejor_cerebro.json")
    print("Usando cerebro entrenado")
    for _ in range(3):
        game.individues.append(Neural(brain=cerebro.mutar()))
else:
    print("No hay cerebro entrenado, usando random")
    for _ in range(3):
        game.individues.append(Neural())


"""for i in range(5):
    game.individues.append(Neural())"""

game.start()