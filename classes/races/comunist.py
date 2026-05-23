from classes.individue import Individues
from classes.action import ActionType
import random

class Comunist(Individues):
    shared_food = 0
    total_comunists = 0
    def __init__(self):
        super().__init__(
            reproduce= 2.5,
            eat_food=2,
            color = "#DE0000"
        )
        Comunist.total_comunists += 1
        self.alive = True
        self.name = "Comunist"
    
    def action(self, other:Individues = None) -> ActionType:
        if other:
            if other.name == self.name:
                return ActionType.SHARE  
        x = random.random()
        if x < 0.5:
            return ActionType.SHARE    
        return ActionType.STEAL
    
    def eat(self):
        if self.can_eat():
            if self.days_without_eating+1 >= self.max_days_without_eating:
                
                #print(f'ÑAM ÑAM ÑAM ÑAM {self.days_without_eating}/{self.max_days_without_eating}')
                Comunist.shared_food  -= self.eat_food
                self.days_without_eating = 0
            else:
                self.days_without_eating +=1
        else:
            self.days_without_eating +=1

    def reproduce(self):
        if self.can_reproduce() and self.days_without_eating == 0:
            Comunist.shared_food -= self.reproduction_food
            childs = []
            for i in range(self.number_children):
                child = self.__class__()
                child.food = 0
                child.days_without_eating = 0
                child.reproduction_food = self.reproduction_food
                child.eat_food = self.eat_food
                child.mutation_rate = self.mutation_rate
                child.mutate()
                childs.append(child)
                
            return childs
        else:
            return None
    
    def survive(self) -> bool:
        survive = super().survive()
    
        if not survive and self.alive:
            self.alive = False
            Comunist.total_comunists -= 1

        return survive
    
    def can_eat(self) -> bool:
        result = Comunist.shared_food > self.eat_food
        return result
    
    def can_reproduce(self) -> bool:
        if Comunist.total_comunists <= 0:
            return False
        return Comunist.shared_food/Comunist.total_comunists >= self.reproduction_food

    def add_food(self,n:int):
        Comunist.shared_food += n
