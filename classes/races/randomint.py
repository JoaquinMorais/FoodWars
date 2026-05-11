from classes.individue import Individues
from classes.action import ActionType
import random

class Randomint(Individues):
    def __init__(self):
        super().__init__(
            color = "#6BBFAA"
        )

        self.name = "Randomint"
    
    def action(self, other:Individues = None) -> ActionType:
        x = random.random()
        if x < 0.5:
            return ActionType.SHARE
        
        return ActionType.STEAL