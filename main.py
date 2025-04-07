import numpy as np
from src.car_agent import Car
from src.track_analysis import load_track
from src.genetic_algorithm import generate_new_population, select_top
from src.simulation import simulate_generation

image_path = "data/test_circuit.png"
track = load_track(image_path)

num_cars = 20
dna_length = 150

population = [Car(dna=Car.generate_dna(size=dna_length)) for _ in range(num_cars)]

generation = 0
history = []

try:
    while True:
        generation += 1
        print(f"\n🧬 Generation {generation}")

        simulate_generation(population, track, background_path=image_path, wait_at_end=False)

        population.sort(key=lambda c: c.fitness, reverse=True)
        best = population[0]
        print(f"🏆 Best Car: {best.fitness:.2f}% progress")

        history.append(best.fitness)

        top = select_top(population, k=5)
        new_population = generate_new_population(top, n=num_cars - 1)
        new_population.append(best) 
        population = new_population

except KeyboardInterrupt:
    print("\n⏹️ Execução interrompida manualmente.")
