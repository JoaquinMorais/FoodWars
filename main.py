from classes.game import Game
from classes.action import ActionType
from classes.races.predator import Predator

"""ind = Predator()
print(ind.eat())
print(ind.can_eat())
print(ind.days_without_eating)"""

game = Game()
for i in range (1000):
    game.simulate_one_day()
game.graph()