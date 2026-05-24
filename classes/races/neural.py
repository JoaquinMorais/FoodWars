from __future__ import annotations
import numpy as np
from classes.individue import Individues
from classes.action import ActionType
import json

NAME_RACES = {
    "Human": 0.0,
    "Predator": 0.1,
    "Prey": 0.2,
    "Ant": 0.3,
    "Bee": 0.4,
    "Dog": 0.5,
    "Mimic": 0.6,
    "Viltrumite": 0.7,
    "Comunist": 0.8,
    "Randomint": 0.9,
    "Neural": 1.0
}

class Neural(Individues):

    def __init__(self, brain: NeuralBrain = None):
        super().__init__(
            reproduce=2.5,
            eat_food=1.75,
            max_days_without_eating=2,
            number_children=1,
            color="#0FC8FF",
        )
        self.name = "Neural"
        self.brain = brain if brain is not None else NeuralBrain()
        self.hijos_totales = 0

    def _build_inputs(self, other: Individues = None, contexto:float = 0.0) -> np.ndarray:
        rival_name = 0.0
        rival_hambre = 0.0
        if other:
            for race, value in NAME_RACES.items():
                if race in other.name:
                    rival_name = value
                    break
            rival_hambre = other.days_without_eating / self.max_days_without_eating

        return np.array([
            self.food / 4,
            self.days_without_eating / self.max_days_without_eating,
            self.food / self.reproduction_food,
            rival_name,
            rival_hambre,
            contexto #0 -> Accion 0.5-> Si comer 1->si Reproducir
        ])

    def action(self, other: Individues = None) -> ActionType:
        entradas = self._build_inputs(other, contexto=0.0)
        resultado = self.brain.forward(entradas)
        return ActionType.SHARE if resultado > 0.5 else ActionType.STEAL

    def eat(self):
        if self.can_eat():
            entradas = self._build_inputs(None, contexto=0.5)
            resultado = self.brain.forward(entradas)
            if resultado > 0.5:
                self.food -= self.eat_food
                self.days_without_eating = 0
            else:
                self.days_without_eating += 1
        else:
            self.days_without_eating += 1

    def reproduce(self):
        if self.can_reproduce() and self.days_without_eating == 0:
            entradas = self._build_inputs(None, contexto=1.0)
            resultado = self.brain.forward(entradas)
            if resultado > 0.5:
                self.food -= self.reproduction_food
                child_brain = self.brain.mutar()
                child = Neural(brain=child_brain)
                self.hijos_totales += 1
                return [child]
        return None



class NeuralBrain:

    def __init__(self):
        # 5 entradas, 6 neuronas ocultas, 1 salida
        self.W1 = np.random.randn(16, 6) * 0.5
        self.b1 = np.zeros(16)
        self.W2 = np.random.randn(8, 16) * 0.5   # segunda capa oculta
        self.b2 = np.zeros(8)    
        self.W3 = np.random.randn(1, 8) * 0.5
        self.b3 = np.zeros(1)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, entradas):
        # entradas es un array de 5 números
        capa_oculta1 = np.tanh(np.dot(self.W1, entradas) + self.b1)
        capa_oculta2 = np.tanh(np.dot(self.W2, capa_oculta1) + self.b2)
        salida = self._sigmoid(np.dot(self.W3, capa_oculta2) + self.b3)
        return salida[0]  # un solo número entre 0 y 1

    def mutar(self, sigma=0.05):
        hijo = NeuralBrain()
        hijo.W1 = self.W1 + np.random.randn(*self.W1.shape) * sigma
        hijo.b1 = self.b1 + np.random.randn(*self.b1.shape) * sigma
        hijo.W2 = self.W2 + np.random.randn(*self.W2.shape) * sigma
        hijo.b2 = self.b2 + np.random.randn(*self.b2.shape) * sigma
        hijo.W3 = self.W3 + np.random.randn(*self.W3.shape) * sigma
        hijo.b3 = self.b3 + np.random.randn(*self.b3.shape) * sigma
        return hijo
    

    def guardar(self, path: str):
        datos = {
            "W1": self.W1.tolist(),  # numpy array → lista normal para poder guardarlo
            "b1": self.b1.tolist(),
            "W2": self.W2.tolist(),
            "b2": self.b2.tolist(),
            "W3": self.W3.tolist(),
            "b3": self.b3.tolist(),
        }
        with open(path, "w") as f:
            json.dump(datos, f)
        print(f"Cerebro guardado en {path}")

    @classmethod
    def cargar(cls, path: str):
        with open(path) as f:
            datos = json.load(f)
        cerebro = cls()
        cerebro.W1 = np.array(datos["W1"])  # lista → numpy array
        cerebro.b1 = np.array(datos["b1"])
        cerebro.W2 = np.array(datos["W2"])
        cerebro.b2 = np.array(datos["b2"])
        cerebro.W3 = np.array(datos["W3"])
        cerebro.b3 = np.array(datos["b3"])
        print(f"Cerebro cargado desde {path}")
        return cerebro



