import random
from collections import Counter
import matplotlib.pyplot as plt
import os

from classes.action import ActionType
from classes.individue import Individues
from classes.races.all import *

def clear():
    os.system("cls" if os.name == "nt" else "clear")

class Game():
    def __init__(self,
        trees:int = 50, #Cuantos arboles hay
        fruits:int = 4, #Cuantos frutos tiene cada arbol
    ):
        self.trees:int = trees
        self.fruits:int = fruits

        self.individues:list[Individues] = []
        """for i in range(10):
            self.individues.append(Human())
            self.individues.append(Predator())
            self.individues.append(Dog())"""
        self.history = []
        self.day = 0

        self.races = [Prey(), Predator(), Human(), Randomint(), Ant, Bee(), Mimic(), 
                      Dog(), Viltrumite(), Comunist()]
        Comunist.total_comunists = 0

        # MATRIZ DE RESULTADOS
        self.rules = {
            (ActionType.SHARE, ActionType.SHARE): (0.5, 0.5),
            (ActionType.STEAL, ActionType.SHARE): (0.75, 0.25),
            (ActionType.SHARE, ActionType.STEAL): (0.25, 0.75),
            (ActionType.STEAL, ActionType.STEAL): (0, 0),

            (ActionType.GIVE_ALL, ActionType.GIVE_ALL): (0, 0),
            (ActionType.GIVE_ALL, ActionType.SHARE): (0, 1),
            (ActionType.SHARE, ActionType.GIVE_ALL): (1, 0),
            (ActionType.GIVE_ALL, ActionType.STEAL): (0, 1),
            (ActionType.STEAL, ActionType.GIVE_ALL): (1, 0),
        }



    def fight(self, action1: ActionType, action2: ActionType):
        result = self.rules[(action1, action2)]

        return (
            self.fruits * result[0],
            self.fruits * result[1]
        )
    
    def simulate_one_day(self, do_graph = False):
        individues_actives = self.individues.copy()
        self.individues = []
        random.shuffle(individues_actives)

        final_trees = {x:[None,None] for x in range(self.trees)}
        free_trees = set(range(self.trees))


        #pelear por la comida
        while individues_actives:
            individue = individues_actives.pop()

            if len(free_trees) == 0:
                break

            tree = random.choice(tuple(free_trees))

            if final_trees[tree][0] is None:
                final_trees[tree][0] = individue

            else:
                final_trees[tree][1] = individue
                free_trees.discard(tree)


        for tree in final_trees:
            ind1 = final_trees[tree][0]
            ind2 = final_trees[tree][1]

            if ind1 is None:
                continue

            elif ind2 is None:
                ind1.add_food(self.fruits)
                self.individues += [ind1]

            else:
                result = self.fight(ind1.action(other = ind2), ind2.action(other = ind1))
                ind1.add_food(result[0])
                ind2.add_food(result[1])
                self.individues += [ind1, ind2]
        self.individues += individues_actives

        new_population = []
        while self.individues:
            individue = self.individues.pop(0)

            individue.eat()

            sons = individue.reproduce()
            if sons is not None:
                new_population += sons

            survive = individue.survive()
            if survive:
                new_population.append(individue)

        self.individues = new_population
        
        if do_graph:
            race_count = Counter(
                individue.name
                for individue in self.individues
            )

            race_colors = {}

            for individue in self.individues:
                race_colors[individue.name] = individue.color


            self.history.append({
                "count": race_count,
                "colors": race_colors
            })

    def graph(self, start=0, end=None, smoothed=False):
        if end is None:
            end = len(self.history)

        history = self.history[start:end]

        all_races = set()

        for day in history:
            all_races.update(day["count"].keys())

        for race in all_races:

            values = []

            for day in history:
                values.append(day["count"].get(race, 0))

            color = next(
                (day["colors"][race] for day in history if race in day["colors"]),
                "black"
            )

            final_values = smooth(values) if smoothed else values

            x = list(range(start, start + len(final_values)))

            plt.plot(
                x,
                final_values,
                color=color
            )

            final_value = values[-1]

            plt.text(
                x[-1] + 1,
                final_values[-1],
                f"{race} ({final_value})",
                fontsize=8,
                color=color
            )

        plt.xlim(right=end + 15)

        plt.show()
        
    def start(self):
        clear()
        print('Iniciando simulacion')
        while True:
            print(f'Dia {self.day}')
            print(f'1) Simular')
            print(f'2) Añadir Poblacion')
            print(f'3) Reiniciar')
            print(f'4) Graficar')
            print(f'5) Mostrar individuos')
            print(f'6) Mostrar razas')
            print(f'7) Salir')
            n = str(input('>> '))
            clear()
            if n == '1':
                print('Cuantos dias desea simular')
                cant = input('>> ')
                initial_day = self.day
                if cant.isnumeric():
                    cant = int(cant)
                    for i in range(cant):
                        self.simulate_one_day(do_graph=True)
                    self.day += cant
                    self.graph(start=initial_day)
            elif n == '2':
                cont = 1
                print('0) Todos')
                for i in self.races:
                    print(f'{cont}) {i.name}')
                    cont += 1

                race = input('>> ')
                if race.isnumeric():
                    race = int(race)
                    if 0 <= race <= len(self.races):
                        print('Cuanta cantidad agregar')
                        cant = input('>> ')
                        if cant.isnumeric():
                            cant = int(cant)
                            if cant >= 1:
                                if race == 5:
                                    self.append_ant(cant)
                                elif race != 0:
                                    self.individues += [self.races[race-1].__class__() for x in range(cant)]
                                else:
                                    for j in self.races:
                                        if j == Ant:
                                            self.append_ant(cant)
                                        else:
                                            self.individues += [
                                                j.__class__()
                                                for x in range(cant)
                                            ]                                        
            elif n == '3':
                self.individues = []
                self.history = []
                self.day = 0
                Ant.total_ants = 0

            elif n == '4':
                self.graph()
            
            elif n == '5':
                cont = 1
                for i in self.individues:
                    print(f'{cont}- {i}')
                    cont += 1
                input('')
            
            elif n == '6':
                actual_races = {}
                for i in self.individues:
                    if i.name in actual_races:
                        actual_races[i.name]['food'] += i.food
                        actual_races[i.name]['eat_food'] += i.eat_food
                        actual_races[i.name]['days_wtout_eat'] += i.days_without_eating
                        actual_races[i.name]['repr_food'] += i.reproduction_food
                        actual_races[i.name]['mut_rate'] += i.mutation_rate
                        actual_races[i.name]['childrens'] += i.number_children
                        actual_races[i.name]['quantity'] += 1
                    else:
                        actual_races[i.name] = {
                            'food':i.food,
                            'eat_food':i.eat_food,
                            'days_wtout_eat':i.days_without_eating,
                            "repr_food":i.reproduction_food,
                            "mut_rate":i.mutation_rate,
                            "childrens" :i.number_children,
                            "quantity":1
                        }
                for i in actual_races:
                    data = [
                        f"{x}:{round(actual_races[i][x]/actual_races[i]['quantity'],2)}"
                        if x != 'quantity'
                        else f"{x}:{actual_races[i][x]}"
                        for x in actual_races[i]
                    ]
                    print(f"{i}: {'|'.join(data)}")
                input('')
            
            elif n=='7':
                break
    

    def append_ant(self, cant:int):
        if cant <= 0:
            return
        ant_type = AntType.QUEEN
        self.individues.append(Ant(ant_type=ant_type))
        for i in range(cant-1):
            x = random.random()
            if x < 0.10:
                ant_type = AntType.WARRIOR
            elif x < 0.20:
                ant_type = AntType.DEFENSIVE
            elif x < 0.99:
                ant_type = AntType.WORKER
            else:
                ant_type = AntType.QUEEN
            self.individues.append(Ant(ant_type=ant_type))

def smooth(values, window=20):

    result = []

    for i in range(len(values)):

        start = max(0, i - window)
        subset = values[start:i+1]

        result.append(
            sum(subset) / len(subset)
        )

    return result
