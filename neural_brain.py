import numpy as np

class NeuralBrain:

    def __init__(self):
        # 5 entradas, 6 neuronas ocultas, 1 salida
        self.W1 = np.random.randn(6, 5) * 0.5
        self.b1 = np.zeros(6)
        self.W2 = np.random.randn(1, 6) * 0.5
        self.b2 = np.zeros(1)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, entradas):
        # entradas es un array de 5 números
        capa_oculta = np.tanh(np.dot(self.W1, entradas) + self.b1)
        salida = self._sigmoid(np.dot(self.W2, capa_oculta) + self.b2)
        return salida[0]  # un solo número entre 0 y 1

    def mutar(self, sigma=0.1):
        hijo = NeuralBrain()
        hijo.W1 = self.W1 + np.random.randn(*self.W1.shape) * sigma
        hijo.b1 = self.b1 + np.random.randn(*self.b1.shape) * sigma
        hijo.W2 = self.W2 + np.random.randn(*self.W2.shape) * sigma
        hijo.b2 = self.b2 + np.random.randn(*self.b2.shape) * sigma
        return hijo
