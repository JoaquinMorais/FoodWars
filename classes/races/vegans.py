from classes.individue import Individues
from classes.action import ActionType

class Vegans(Individues):
    def __init__(self):
        super().__init__(
            color =  "#4ABD00"
        )

        self.name = "Vegans"
    
    def action(self, other:Individues = None) -> ActionType:
        return ActionType.SHARE