from src.track_analysis import load_track
from src.car_agent import Car
from src.simulation import simulate_race
from src.genetic_algorithm import compute_fitness, select_top, generate_new_population
import cv2

track = load_track("data/interlagos.png")
cv2.imshow("Track Mask", track * 255)
cv2.waitKey(0)
cv2.destroyAllWindows()

population = [Car() for _ in range(20)]

for generation in range(10):
    print(f"\nGeneration {generation}")
    for car in population:
        simulate_race(population[0], track, visualize=True, background_path="data/interlagos.png")
        car.fitness = compute_fitness(car)
        print(f"Time: {car.time:.2f} | Penalties: {car.penalties} | Fitness: {car.fitness:.4f}")

    top_cars = select_top(population, k=5)
    population = generate_new_population(top_cars, n=20)
