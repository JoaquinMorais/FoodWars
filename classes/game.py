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
        
        #pelear por la comida
        for tree in range(self.trees):
            if len(individues_actives) == 0:
                break 
            elif len(individues_actives) != 1:
                ind1, ind2 = random.sample(individues_actives, 2)
                individues_actives.remove(ind1)
                individues_actives.remove(ind2)

                result = self.fight(ind1.action(ind2), ind2.action(ind1))
                print(result)
                ind1.food += result[0]
                ind2.food += result[1]

                self.individues += [ind1, ind2]
                
            else:
                ind = individues_actives[0]
                individues_actives.remove(ind)
                ind.food += self.fruits
                self.individues += [ind]

        print(self.individues)

