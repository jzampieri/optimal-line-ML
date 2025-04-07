import numpy as np
import cv2
import random
from .track_analysis import get_start_and_end_points

def generate_colors(n):
    random.seed(42)
    return [
        (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        for _ in range(n)
    ]

def generate_grid_positions(center, total, track_mask, spacing=10, max_radius=100):
    positions = []
    h, w = track_mask.shape
    cx, cy = int(center[0]), int(center[1])

    for r in range(0, max_radius, spacing):
        for dx in range(-r, r + 1, spacing):
            for dy in range(-r, r + 1, spacing):
                x, y = cx + dx, cy + dy
                if len(positions) >= total:
                    return positions
                if 0 <= x < w and 0 <= y < h and track_mask[y, x] == 1:
                    point = np.array([x, y], dtype=np.float32)
                    if not any(np.allclose(point, p) for p in positions):
                        positions.append(point)

    print("⚠️ Warning: not enough valid starting positions. Filling with center.")
    while len(positions) < total:
        positions.append(center.copy())
    return positions

def simulate_generation(cars, track_mask, background_path, wait_at_end=True):
    start_point, end_point = get_start_and_end_points()
    initial_distance = np.linalg.norm(start_point - end_point)

    positions = [start_point.copy() for _ in cars]
    angles = [0.0 for _ in cars]
    velocities = [0.0 for _ in cars]
    paths = [[] for _ in cars]
    active = [True] * len(cars)
    colors = generate_colors(len(cars))

    height, width = track_mask.shape
    background = cv2.imread(background_path)
    canvas = cv2.resize(background, (width, height))

    for car in cars:
        car.time = 0
        car.crashed = False
        car.finished = False
        car.distance = 0.0

    max_steps = max(len(car.dna) for car in cars)
    step_i = 0

    while any(active) and step_i < max_steps:
        for idx, car in enumerate(cars):
            if not active[idx] or step_i >= len(car.dna):
                continue

            accel, turn = car.dna[step_i]
            velocities[idx] += accel
            velocities[idx] = max(0, min(car.max_speed, velocities[idx]))

            angles[idx] += turn
            dx = np.cos(angles[idx]) * velocities[idx]
            dy = np.sin(angles[idx]) * velocities[idx]

            move_vector = np.array([dx, dy])
            next_pos = positions[idx] + move_vector
            x, y = int(next_pos[0]), int(next_pos[1])

            if x < 0 or x >= width or y < 0 or y >= height or track_mask[y, x] != 1:
                print(f"💥 Car {idx} hit the wall and was eliminated.")
                car.crashed = True
                active[idx] = False
                continue

            if np.linalg.norm(next_pos - end_point) < 15:
                print(f"🏁 Car {idx} reached the goal!")
                car.finished = True
                active[idx] = False

            positions[idx] = next_pos
            car.distance += np.linalg.norm(move_vector)
            paths[idx].append((x, y))

        # Desenhar frame
        frame = canvas.copy()
        best_idx = np.argmax([car.distance for car in cars])

        for idx, path in enumerate(paths):
            if not path:
                continue

            # cor do traçado
            line_color = colors[idx] if idx == best_idx else (60, 60, 60)

            for i in range(1, len(path)):
                cv2.line(frame, path[i - 1], path[i], line_color, 4)

            px, py = path[-1]
            angle = angles[idx]

            # desenhar retângulo
            rect_length = 10
            rect_width = 5
            front = np.array([np.cos(angle), np.sin(angle)]) * rect_length / 2
            side = np.array([-np.sin(angle), np.cos(angle)]) * rect_width / 2

            p1 = (int(px + front[0] + side[0]), int(py + front[1] + side[1]))
            p2 = (int(px + front[0] - side[0]), int(py + front[1] - side[1]))
            p3 = (int(px - front[0] - side[0]), int(py - front[1] - side[1]))
            p4 = (int(px - front[0] + side[0]), int(py - front[1] + side[1]))
            pts = np.array([p1, p2, p3, p4], np.int32)
            cv2.fillPoly(frame, [pts], colors[idx])

            # sensores
            sensor_angles = [-np.pi / 4, -np.pi / 8, 0, np.pi / 8, np.pi / 4]
            for delta in sensor_angles:
                sensor_angle = angle + delta
                for dist in range(1, 100):
                    sx = int(px + np.cos(sensor_angle) * dist)
                    sy = int(py + np.sin(sensor_angle) * dist)
                    if 0 <= sx < width and 0 <= sy < height:
                        if track_mask[sy, sx] == 0:
                            break
                        cv2.line(frame, (int(px), int(py)), (sx, sy), (200, 200, 200), 1)
                    else:
                        break

        cv2.imshow("All Cars Simulation", frame)
        cv2.waitKey(30)
        step_i += 1

    print("\n📊 Progress this generation:")
    for idx, car in enumerate(cars):
        dist_to_goal = np.linalg.norm(positions[idx] - end_point)
        progress = max(0, 1 - (dist_to_goal / initial_distance)) * 100
        car.fitness = progress
        print(f"🚗 Car {idx}: {progress:.2f}% progress | Distance to goal: {dist_to_goal:.2f} px")

    if wait_at_end:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()
