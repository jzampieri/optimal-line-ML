import numpy as np

class Car:
    def __init__(self, dna, max_speed=5.0):
        self.dna = dna
        self.max_speed = max_speed

        self.position = None
        self.angle = 0.0
        self.velocity = 0.0
        self.time = 0
        self.penalties = 0
        self.crashed = False
        self.distance = 0.0
        self.fitness = 0.0

    @staticmethod
    def generate_dna(size=150):
        return np.random.uniform(-0.2, 0.2, size=(size, 2))
