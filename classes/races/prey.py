from classes.individue import Individues
from classes.action import ActionType

class Prey(Individues):
    def __init__(self):
        super().__init__(
            color =  "#4ABD00",
            reproduce=1.5
        )

        self.name = "Prey"
    
    def action(self, other:Individues = None) -> ActionType:
        return ActionType.SHARE