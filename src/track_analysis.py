import cv2
import numpy as np

def load_track(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    track_mask = np.zeros_like(mask, dtype=np.uint8)
    track_mask[mask == 255] = 1

    return track_mask

def get_start_and_end_points():
    start_point = np.array([150, 680], dtype=np.float32)
    end_point = np.array([700, 120], dtype=np.float32)
    return start_point, end_point
