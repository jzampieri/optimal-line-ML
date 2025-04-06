import cv2
import numpy as np

def load_track(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, track_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((25, 25), np.uint8)
    dilated = cv2.dilate(track_mask, kernel, iterations=1)

    binary_mask = (dilated > 0).astype(np.uint8)

    return binary_mask
