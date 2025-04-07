import random
import cv2

def detect_edges(image_path):
    img = cv2.imread(image_path, 0)
    edges = cv2.Canny(img, 100, 200)
    return edges

def generate_colors(n):
    random.seed(42)
    return [
        (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        for _ in range(n)
    ]