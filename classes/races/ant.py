from enum import Enum
import random
from classes.individue import Individues
from classes.action import ActionType


class AntType(Enum):
    QUEEN = "queen"
    WORKER = "worker"
    WARRIOR = "warrior"
    DEFENSIVE = "defensive"

    
class Ant(Individues):
    total_ants = 0
    name = 'Ant'

    def __init__(self, ant_type:AntType = AntType.QUEEN):
        
        self.ant_type = ant_type
        if ant_type == AntType.QUEEN:
            n = random.randint(8,12)

            reproduce = n-4
            eat_food = 4
            mutation_rate = 0
            max_days_without_eating = 3
            number_children = n
        else:
            reproduce = 100
            eat_food = 1
            mutation_rate = 0
            max_days_without_eating:int = 1
            number_children = 0

        super().__init__(
            reproduce=reproduce,
            eat_food=eat_food,
            mutation_rate=mutation_rate,
            max_days_without_eating=max_days_without_eating,
            number_children=number_children,
            color =  "#0F0F0F",
        )
        self.name = f"Ant({ant_type.value.title()})"
        self.alive = True

        Ant.total_ants += 1
    
    def action(self, other:Individues = None) -> ActionType:
        # Entre hormigas siempre SHARE
        if isinstance(other, Ant):
            necessary_food = self.eat_food * self.max_days_without_eating
            if other.ant_type == AntType.QUEEN and self.ant_type != AntType.QUEEN:
                if self.food > necessary_food:
                    other.food += self.food - necessary_food
                    self.food = necessary_food
                    
                return ActionType.GIVE_ALL
            return ActionType.SHARE

        # Reina
        if self.ant_type == AntType.QUEEN:
            return ActionType.SHARE

        # Obrera
        if self.ant_type == AntType.WORKER:
            if Ant.total_ants > 40:
                if random.random() < 0.5:
                    return ActionType.STEAL
            return ActionType.SHARE

        # Guerrera
        if self.ant_type == AntType.WARRIOR:
            if Ant.total_ants < 40:
                if random.random() < 0.5:
                    return ActionType.SHARE
            return ActionType.STEAL

        # Defensiva
        if self.ant_type == AntType.DEFENSIVE:

            if Ant.total_ants > 50:
                return ActionType.STEAL
            else:
                return ActionType.SHARE
    
    def survive(self) -> bool:
        survive = super().survive()
    
        if not survive and self.alive:
            self.alive = False
            Ant.total_ants -= 1

        return survive
    
    def reproduce(self):
        if self.ant_type != AntType.QUEEN:
            return None
        
        if self.can_reproduce() and self.days_without_eating == 0:
            childs = []
            self.food -= self.reproduction_food

            for i in range(self.number_children):
                x = random.random()
                if x < 0.10:
                    ant_type = AntType.WARRIOR
                elif x < 0.20:
                    ant_type = AntType.DEFENSIVE
                elif x < 0.99:
                    ant_type = AntType.WORKER
                else:
                    ant_type = AntType.QUEEN

                child = self.__class__(ant_type=ant_type)
                child.food = 0
                child.days_without_eating = 0
                child.mutate()

                childs.append(child)

            return childs
        else:
            return None

