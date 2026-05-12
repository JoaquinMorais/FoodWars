from classes.individue import Individues
from classes.action import ActionType

class Bee(Individues):
    def __init__(self):
        super().__init__(
            color =  "#FFE000",
            reproduce= 2,
            eat_food=1.2,
            max_days_without_eating=1
        )

        self.name = "Bee"
    
    def action(self, other:Individues = None) -> ActionType:
        if isinstance(other, Bee):
            return ActionType.SHARE
        return ActionType.STEAL