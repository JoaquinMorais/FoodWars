from classes.action import ActionType

class Game():
    def __init__(self,
        trees:int = 50, #Cuantos arboles hay
        fruits:int = 2, #Cuantos frutos tiene cada arbol
    ):
        self.trees = trees,
        self.fruits = fruits
        
    def fight(self, action1: ActionType, action2: ActionType):

        print(action1)
        print(action1.value)

        if action1 == ActionType.STEAL:
            print("Player 1 steals")

        if action2 == ActionType.SHARE:
            print("Player 2 shares")
