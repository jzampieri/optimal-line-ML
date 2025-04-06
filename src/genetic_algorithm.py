import numpy as np
from src.car_agent import Car

def compute_fitness(car):
    if car.crashed:
        return 0
    return 1 / (car.time + 1 + car.penalties)

def select_top(population, k=5):
    return sorted(population, key=lambda c: c.fitness, reverse=True)[:k]

def crossover(parent1, parent2):
    point = np.random.randint(0, len(parent1.dna))
    child_dna = np.vstack((parent1.dna[:point], parent2.dna[point:]))
    return Car(dna=child_dna)

def mutate(car, mutation_rate=0.1):
    new_dna = np.copy(car.dna)
    for i in range(len(new_dna)):
        if np.random.rand() < mutation_rate:
            new_dna[i] += np.random.uniform(-0.2, 0.2, size=2)
    return Car(dna=new_dna)

def generate_new_population(top_cars, n=20):
    new_population = []
    while len(new_population) < n:
        parent1, parent2 = np.random.choice(top_cars, 2)
        child = crossover(parent1, parent2)
        child = mutate(child)
        new_population.append(child)
    return new_population
