from abc import ABC, abstractmethod

class Individues(ABC):
    def __init__(self, reproduce:float = 1.5, survival:float = 1):
        self.name = 'base'
        self.food:float = 0
        self.reproduction_food:float = reproduce
        self.survival_food:float = survival


    def can_survive(self) -> bool:
        return self.food >= self.survival_food()
    
    def can_reproduce(self) -> bool:
        return self.food >= self.reproduction_food()
    

