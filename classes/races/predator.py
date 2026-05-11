from classes.individue import Individues
from classes.action import ActionType

class Predator(Individues):
    def __init__(self):
        super().__init__(
            reproduce=1.5,
            eat=1.5,
            mutation_rate=0,

            min_amount_reproduction_food=1,
            min_amount_eat_food=1,

            max_days_without_eating=2
        )

        self.name = "Predator"
    
    def action(self, other:Individues) -> ActionType:
        return ActionType.STEAL