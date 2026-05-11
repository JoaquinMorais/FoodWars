import random
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
        print(individues_actives)
        while individues_actives:
            individue = individues_actives.pop()
            print(individue)

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
                print(f'{ind1} eat all')

            else:
                result = self.fight(ind1.action(ind2), ind2.action(ind1))
                print(result)
                ind1.food += result[0]
                ind2.food += result[1]
                self.individues += [ind1, ind2]
        self.individues += individues_actives

        

                

