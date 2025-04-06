import cv2
import numpy as np

def load_track(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, base_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    inner_mask = base_mask.copy()

    kernel_outer = np.ones((25, 25), np.uint8)
    outer_mask = cv2.dilate(base_mask, kernel_outer, iterations=1)

    final_mask = np.zeros_like(gray, dtype=np.uint8)

    final_mask[inner_mask == 255] = 1

    penalty_zone = ((outer_mask == 255) & (inner_mask == 0))
    final_mask[penalty_zone] = 2

    return final_mask
