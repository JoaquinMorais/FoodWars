from classes.individue import Individues
from classes.action import ActionType
import random

class Dog(Individues):
    def __init__(self):
        super().__init__(
            reproduce= 4,
            eat_food=2,
            color = "#A14100",
            number_children=random.randint(1,2)
        )

        self.name = "Dog"
    
    def action(self, other:Individues = None) -> ActionType:
        if other:
            if other.name in ['Human','Dog']:
                return ActionType.SHARE
        else:
            x = random.random()
            if x < 0.5:
                return ActionType.SHARE
        return ActionType.STEAL