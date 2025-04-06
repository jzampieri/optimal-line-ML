import numpy as np
from src.car_agent import Car
from src.track_analysis import load_track
from src.genetic_algorithm import generate_new_population, select_top
from src.multi_simulation import simulate_generation

# 📁 Caminho para a imagem do traçado
image_path = "data/interlagos.png"
track = load_track(image_path)

# ⚙️ Parâmetros
num_cars = 20
num_generations = 50
dna_length = 150

population = [Car(dna=Car.generate_dna(size=dna_length)) for _ in range(num_cars)]

for generation in range(num_generations):
    print(f"\n🧬 Generation {generation + 1}/{num_generations}")

    simulate_generation(population, track, background_path=image_path, wait_at_end=False)

    population.sort(key=lambda c: c.fitness, reverse=True)

    best = population[0]
    print(f"\n🏆 Best of Generation {generation + 1}: {best.distance:.2f} m | Penalties: {best.penalties} | Fitness: {best.fitness:.2f}")

    top = select_top(population, k=5)
    new_population = generate_new_population(top, n=num_cars - 1)
    new_population.append(best) 
    population = new_population
