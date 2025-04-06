import numpy as np
import cv2

def simulate_race(car, track_mask, visualize=False, background_path="data/image.png"):
    height, width = track_mask.shape
    position = np.array([width // 2, height // 2], dtype=np.float32)

    car.time = 0
    car.penalties = 0
    car.crashed = False

    if visualize:
        background = cv2.imread(background_path)
        canvas = cv2.resize(background, (width, height))

    for step in car.dna:
        direction = step * 10  # Scale movement
        position += direction
        x, y = int(position[0]), int(position[1])

        if x < 0 or x >= width or y < 0 or y >= height:
            car.crashed = True
            car.time = 0
            break

        pixel = track_mask[y, x]

        if pixel == 1:
            car.time += 1
            color = (0, 255, 0)  # green
        else:
            car.time += 2
            car.penalties += 1
            color = (0, 0, 255)  # red
            if car.penalties > 5:
                car.crashed = True
                car.time = 0
                break

        if visualize:
            cv2.circle(canvas, (x, y), 2, color, -1)
            cv2.imshow("Car Simulation", canvas)
            cv2.waitKey(30)

    if visualize:
        cv2.waitKey(500)
        cv2.destroyAllWindows()
