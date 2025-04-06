import numpy as np
import cv2

def simulate_race(car, track_mask, visualize=False, background_path="../data/interlagos.png"):
    height, width = track_mask.shape

    car.time = 0
    car.penalties = 0
    car.crashed = False

    if visualize:
        background = cv2.imread(background_path)

        if background is None:
            # fallback: mostra a máscara da pista se a imagem falhar
            canvas = cv2.cvtColor(track_mask * 127, cv2.COLOR_GRAY2BGR)
            print("⚠️ Warning: background image not loaded, using track mask.")
        else:
            canvas = cv2.resize(background, (width, height))


    for step in car.dna:
        direction = step * 0.5
        position += direction
        x, y = int(position[0]), int(position[1])

        if x < 0 or x >= width or y < 0 or y >= height:
            car.crashed = True
            car.time = 0
            break

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
        else:
            print(f"💥 Car {idx} went off track and was eliminated immediately.")
            car.crashed = True
            active[idx] = False


        if visualize:
            cv2.circle(canvas, (x, y), 2, color, -1)
            cv2.imshow("Car Simulation", canvas)
            cv2.waitKey(30)

    if visualize:
        cv2.waitKey(500)
        cv2.destroyAllWindows()
