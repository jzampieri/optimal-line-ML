import numpy as np

class Car:
    def __init__(self, dna=None):
        self.dna = dna if dna is not None else self.generate_dna()
        self.time = 0
        self.penalties = 0
        self.crashed = False
        self.fitness = 0

    def generate_dna(self, size=50):
        return np.random.uniform(-1, 1, size=(size, 2))
