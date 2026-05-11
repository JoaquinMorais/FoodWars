import random
from collections import Counter
import matplotlib.pyplot as plt

from classes.action import ActionType
from classes.individue import Individues
from classes.races.all import *

class Game():
    def __init__(self,
        trees:int = 50, #Cuantos arboles hay
        fruits:int = 4, #Cuantos frutos tiene cada arbol
    ):
        self.trees:int = trees
        self.fruits:int = fruits

        self.individues:list[Individues] = [Predator(),Predator(),Predator(),Vegans(),Vegans(),Vegans(),Vegans()]
        self.history = []

        # MATRIZ DE RESULTADOS
        self.rules = {
            
            (ActionType.SHARE, ActionType.SHARE): (0.5, 0.5),
            (ActionType.STEAL, ActionType.SHARE): (0.75, 0.25),
            (ActionType.SHARE, ActionType.STEAL): (0.25, 0.75),
            (ActionType.STEAL, ActionType.STEAL): (0, 0),
        }



    def fight(self, action1: ActionType, action2: ActionType):
        result = self.rules[(action1, action2)]

        return (
            self.fruits * result[0],
            self.fruits * result[1]
        )
    
    def simulate_one_day(self):
        individues_actives = self.individues.copy()
        self.individues = []
        random.shuffle(individues_actives)

        final_trees = {x:[None,None] for x in range(self.trees)}
        free_trees = [x for x in range(self.trees)]

        #pelear por la comida
        while individues_actives:
            individue = individues_actives.pop()

            if len(free_trees) == 0:
                break

            tree = random.choice(free_trees)

            if final_trees[tree][0] is None:
                final_trees[tree][0] = individue

            else:
                final_trees[tree][1] = individue
                free_trees.remove(tree)


        for tree in final_trees:
            ind1 = final_trees[tree][0]
            ind2 = final_trees[tree][1]

            if ind1 is None:
                continue

            elif ind2 is None:
                ind1.food += self.fruits
                self.individues += [ind1]

            else:
                result = self.fight(ind1.action(other = ind2), ind2.action(other = ind1))
                ind1.food += result[0]
                ind2.food += result[1]
                self.individues += [ind1, ind2]
        self.individues += individues_actives

        new_population = []
        while self.individues:
            individue = self.individues.pop(0)

            individue.eat()

            son = individue.reproduce()
            if son is not None:
                new_population.append(son)

            survive = individue.survive()
            if survive:
                new_population.append(individue)

        self.individues = new_population
        
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

    def graph(self):
        all_races = set()

        for day in self.history:
            all_races.update(day["count"].keys())


        for race in all_races:

            values = []

            for day in self.history:
                values.append(day["count"].get(race, 0))

            color = self.history[0]["colors"][race]

            smooth_values = smooth(values)

            plt.plot(
                smooth_values,
                label=race,
                color=color
            )

        plt.legend()
        plt.show()


def smooth(values, window=20):

    result = []

    for i in range(len(values)):

        start = max(0, i - window)
        subset = values[start:i+1]

        result.append(
            sum(subset) / len(subset)
        )

    return result