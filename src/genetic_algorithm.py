import numpy as np
import random
from src.car_agent import Car

def compute_fitness(car):
    if car.crashed:
        return 0
    return car.time - car.penalties * 2

def select_top(cars, k=5):
    sorted_cars = sorted(cars, key=lambda c: c.fitness, reverse=True)
    return sorted_cars[:k]


def crossover(parent1, parent2):
    point = np.random.randint(0, len(parent1.dna))
    child_dna = np.vstack((parent1.dna[:point], parent2.dna[point:]))
    return Car(dna=child_dna)

def mutate_dna(dna, mutation_rate=0.1, mutation_strength=0.5):
    new_dna = dna.copy()
    for i in range(len(dna)):
        if np.random.rand() < mutation_rate:
            new_dna[i] += np.random.uniform(-mutation_strength, mutation_strength, size=2)
    return new_dna

def generate_new_population(top_cars, n):
    from src.car_agent import Car
    new_population = []
    for _ in range(n):
        parent = np.random.choice(top_cars)
        new_dna = mutate_dna(parent.dna)
        new_population.append(Car(dna=new_dna))
    return new_population

def select_top(population, k=5):
    return sorted(population, key=lambda c: c.fitness, reverse=True)[:k]