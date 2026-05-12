from classes.individue import Individues
from classes.action import ActionType
import random

class Human(Individues):
    def __init__(self):
        super().__init__(
            reproduce= 2.5,
            color = "#BABABA"
        )

        self.name = "Human"
    
    def action(self, other:Individues = None) -> ActionType:
        if other:
            other_action = other.action()
            if other_action == ActionType.STEAL:
                return ActionType.SHARE
        else:
            x = random.random()
            if x < 0.5:
                return ActionType.SHARE
        
        return ActionType.STEAL