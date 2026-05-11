from classes.individue import Individues
from classes.action import ActionType

class Predator(Individues):
    def __init__(self):
        super().__init__(
            reproduce = 2,
            color =  "#DE2C09"
        )

        self.name = "Predator"
    
    def action(self, other:Individues = None) -> ActionType:
        return ActionType.STEAL