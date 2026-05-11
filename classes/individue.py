from __future__ import annotations
import random
from classes.action import ActionType

class Individues():
    def __init__(self, 
            reproduce:float = 1.5, 
            eat:float = 1.5,
            mutation_rate:float = 0,
            min_amount_reproduction_food:float = 0.5,
            min_amount_eat_food:float = 0.5,
            max_days_without_eating:int = 2,
            color:str = "#ff0000"
        ):
        self.name = 'base'
        self.food:float = 0
        self.days_without_eating:int = 0

        self.reproduction_food:float = reproduce
        self.eat_food:float = eat
        self.mutation_rate:float = mutation_rate

        self.min_amount_reproduction_food:float = min_amount_reproduction_food
        self.min_amount_eat_food:float = min_amount_eat_food

        self.max_days_without_eating:int = max_days_without_eating

        self.color = color
    
    def __repr__(self):
        return f'{self.name}:{self.food}'

    def action(self, other:Individues = None) -> ActionType:
        pass

    def eat(self):
        if self.can_eat():
            self.food -= self.eat_food
            self.days_without_eating = 0
        else:
            self.days_without_eating +=1
            
    def survive(self) -> bool:
        if self.days_without_eating >= self.max_days_without_eating:
            return False
        return True

    def reproduce(self):
        if self.can_reproduce():
            self.food -= self.reproduction_food

            child = self.__class__()
            child.food = 0
            child.days_without_eating = 0
            child.mutate()

            return child
        else:
            return None
    
    def mutate(self):
        if self.mutation_rate > 0:
            x = random.random()
            if x < self.mutation_rate:
                self.reproduction_food = max(self.get_mutation(self.reproduction_food), self.min_amount_reproduction_food)
                self.eat_food = max(self.get_mutation(self.eat_food), self.min_amount_eat_food)
                self.mutation_rate = max(self.get_mutation(self.mutation_rate),0)

    def can_eat(self) -> bool:
        result = self.food > self.eat_food
        return result
    
    def can_reproduce(self) -> bool:
        return self.food >= self.reproduction_food
    
    def get_mutation(self, actual_amount, max_amount = 4) -> float:
        x = random.uniform(-self.mutation_rate, self.mutation_rate) * random.randint(1,max_amount)
        return actual_amount*(1+x)

