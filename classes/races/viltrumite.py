from classes.individue import Individues
from classes.action import ActionType
import random

class Viltrumite(Individues):
    def __init__(self):
        super().__init__(
            reproduce= 40,
            eat_food=60,
            max_days_without_eating=random.randint(45,55),
            color = "#BABABA"
        )

        self.name = "Viltrumite"
    
    def action(self, other:Individues = None) -> ActionType:
        return ActionType.STEAL
    
    def reproduce(self):
        child = super().reproduce()
        if not child:
            return None
        child = child[0]
        child.max_days_without_eating = self.max_days_without_eating
        return [child]