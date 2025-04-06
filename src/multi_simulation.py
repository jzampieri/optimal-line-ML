import numpy as np
import cv2
import random

def get_sensor_endpoints(position, angle, track_mask, max_distance=100):
    sensor_angles = [-np.pi / 4, -np.pi / 8, 0, np.pi / 8, np.pi / 4]
    endpoints = []
    h, w = track_mask.shape

    for delta_angle in sensor_angles:
        sensor_angle = angle + delta_angle
        end = position.copy()

        for d in range(1, max_distance):
            x = int(position[0] + np.cos(sensor_angle) * d)
            y = int(position[1] + np.sin(sensor_angle) * d)

            if 0 <= x < w and 0 <= y < h:
                if track_mask[y, x] == 0:
                    break
                end = np.array([x, y])
            else:
                break

        endpoints.append(end)

    return endpoints


def generate_colors(n):
    random.seed(42)
    return [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(n)]

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
                if 0 <= x < w and 0 <= y < h and track_mask[y, x] == 255:
                    point = np.array([x, y], dtype=np.float32)
                    if not any(np.allclose(point, p) for p in positions):
                        positions.append(point)

    print("⚠️ Warning: not enough valid starting positions. Filling with center.")
    while len(positions) < total:
        positions.append(center.copy())
    return positions

def get_sensor_distances(position, angle, track_mask, max_distance=100):
    sensor_angles = [-np.pi / 4, -np.pi / 8, 0, np.pi / 8, np.pi / 4]
    distances = []
    h, w = track_mask.shape

    for delta_angle in sensor_angles:
        sensor_hit_point = position.copy()
        sensor_angle = angle + delta_angle

        for d in range(1, max_distance):
            test_x = int(position[0] + np.cos(sensor_angle) * d)
            test_y = int(position[1] + np.sin(sensor_angle) * d)

            if 0 <= test_x < w and 0 <= test_y < h:
                if track_mask[test_y, test_x] == 0:
                    break
                sensor_hit_point = np.array([test_x, test_y])
            else:
                break

        sensor_lines.append(sensor_hit_point)

    return distances

PIXEL_TO_METERS = 1.52

def get_sensor_endpoints(position, angle, track_mask, max_distance=100):
    sensor_angles = [-np.pi / 4, -np.pi / 8, 0, np.pi / 8, np.pi / 4]
    endpoints = []
    h, w = track_mask.shape

    for delta_angle in sensor_angles:
        sensor_angle = angle + delta_angle
        end = position.copy()

        for d in range(1, max_distance):
            x = int(position[0] + np.cos(sensor_angle) * d)
            y = int(position[1] + np.sin(sensor_angle) * d)

            if 0 <= x < w and 0 <= y < h:
                if track_mask[y, x] == 0:
                    break
                end = np.array([x, y])
            else:
                break

        endpoints.append(end)

    return endpoints

def generate_colors(n):
    random.seed(42)
    return [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(n)]

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
                if 0 <= x < w and 0 <= y < h and track_mask[y, x] == 255:
                    point = np.array([x, y], dtype=np.float32)
                    if not any(np.allclose(point, p) for p in positions):
                        positions.append(point)

    print("⚠️ Warning: not enough valid starting positions. Filling with center.")
    while len(positions) < total:
        positions.append(center.copy())
    return positions

def simulate_generation(cars, track_mask, background_path="data/image.png", wait_at_end=True):
    start_center = np.array([424, 275], dtype=np.float32)
    positions = generate_grid_positions(start_center, len(cars), track_mask, spacing=12)

    angles = [0.0 for _ in cars]
    velocities = [0.0 for _ in cars]
    paths = [[] for _ in cars]
    active = [True] * len(cars)
    colors = generate_colors(len(cars))

    height, width = track_mask.shape
    background = cv2.imread(background_path)
    canvas = cv2.resize(background, (width, height))

    max_steps = max(len(car.dna) for car in cars)

    for car in cars:
        car.time = 0
        car.penalties = 0
        car.crashed = False
        car.distance = 0.0

    for step_i in range(max_steps):
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

            if x < 0 or x >= width or y < 0 or y >= height:
                car.crashed = True
                active[idx] = False
                continue

            zone = track_mask[y, x]

            if zone == 1:
                car.time += 1
            elif zone == 2:
                car.time += 1
                car.penalties += 1
                if car.penalties >= 3:
                    print(f"⚠️ Car {idx} received 3 warnings and was eliminated.")
                    car.crashed = True
                    active[idx] = False
                    continue
            else:
                print(f"💥 Car {idx} went off track and was eliminated immediately.")
                car.crashed = True
                active[idx] = False
                continue

            expected_direction = np.array([0, -1])
            movement_unit = move_vector / (np.linalg.norm(move_vector) + 1e-6)
            cos_angle = np.dot(movement_unit, expected_direction)

            if cos_angle < 0:
                continue 

            positions[idx] = next_pos
            car.distance += np.linalg.norm(move_vector) * PIXEL_TO_METERS
            paths[idx].append((x, y))

        frame = canvas.copy()
        for idx, path in enumerate(paths):
            if not path:
                continue
            for i in range(1, len(path)):
                cv2.line(frame, path[i - 1], path[i], colors[idx], 2)

            px, py = path[-1]
            angle = angles[idx]

            length = 6
            rear_width = 3
            tip = (int(px + np.cos(angle) * length), int(py + np.sin(angle) * length))
            left = (int(px + np.cos(angle + np.pi * 0.75) * rear_width),
                    int(py + np.sin(angle + np.pi * 0.75) * rear_width))
            right = (int(px + np.cos(angle - np.pi * 0.75) * rear_width),
                     int(py + np.sin(angle - np.pi * 0.75) * rear_width))
            pts = np.array([tip, left, right], np.int32)
            cv2.fillPoly(frame, [pts], colors[idx])

            sensor_ends = get_sensor_endpoints(np.array([px, py]), angle, track_mask)
            for end in sensor_ends:
                ex, ey = int(end[0]), int(end[1])
                cv2.line(frame, (int(px), int(py)), (ex, ey), (255, 255, 255), 1)

        leader_idx = np.argmax([car.distance for car in cars])
        cx, cy = positions[leader_idx].astype(int)
        zoom_size = 250

        top = max(0, cy - zoom_size)
        bottom = min(height, cy + zoom_size)
        left = max(0, cx - zoom_size)
        right = min(width, cx + zoom_size)

        view = frame[top:bottom, left:right]
        zoomed = cv2.resize(view, (width, height), interpolation=cv2.INTER_LINEAR)
        cv2.imshow("All Cars Simulation", zoomed)
        cv2.waitKey(30)

    print("\n📊 Distâncias desta geração:")
    for idx, car in enumerate(cars):
        car.fitness = car.distance - (car.penalties * 10)
        print(f"🔵 Car {idx}: Distance = {car.distance:.2f} m | Penalties: {car.penalties} | Fitness: {car.fitness:.2f}")

    if wait_at_end:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()
