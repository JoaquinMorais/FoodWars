from classes.races.neural import Neural
from classes.races.prey import Prey


neural = Neural()
prey = Prey()
prey.food = 3

print(f'Accion vs rival: {neural.action(other=prey)}')
print(f'Accion solo: {neural.action(other=None)}')


neural.food = 5
print('comer 5')
print(f'Comida antes: {neural.food}')
neural.eat()
print(f'food despues: {neural.food}')
print(f'dias sin comer: {neural.days_without_eating}')

neural.food = 10
print('comer 10')
hijo = neural.reproduce()
if hijo:
    print(f'tuvo un hijo: {hijo}')
    print(f'comida despues de reproducirse: {neural.food}')
else:
    print('No la puso')