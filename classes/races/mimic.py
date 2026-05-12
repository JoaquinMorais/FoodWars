from classes.individue import Individues
from classes.action import ActionType
import random

class Mimic(Individues):
    def __init__(self):
        super().__init__(
            reproduce= 2.25,
            color = "#63322E"
        )

        self.name = "Mimic"
    
    def action(self, other:Individues = None) -> ActionType:
        if other:
            other_action = other.action()
            return other_action
        else:
            x = random.random()
            if x < 0.5:
                return ActionType.SHARE
        return ActionType.STEAL