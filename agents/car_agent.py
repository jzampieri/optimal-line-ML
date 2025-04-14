import pygame
import math
import numpy as np

SENSOR_LENGTH = 100

class Car:
    def __init__(self, x, y, angle=0, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.angle = angle 
        self.speed = 2
        self.color = color
        self.width = 10
        self.height = 20
        self.sensors = []
        self.alive = True

    def update(self, screen, track_mask):
        if not self.alive:
            return

        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)
        self._update_sensors(screen, track_mask)

        if self._check_collision(track_mask):
            self.alive = False

        pygame.draw.rect(
            screen, self.color,
            pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        )

    def _update_sensors(self, screen, track_mask):
        self.sensors.clear()
        angles = [-45, -20, 0, 20, 45] 

        for a in angles:
            distance, end_x, end_y = self._cast_sensor(track_mask, a)
            self.sensors.append(((end_x, end_y), distance / SENSOR_LENGTH))
            pygame.draw.line(screen, (180, 180, 180), (self.x, self.y), (end_x, end_y), 1)
            pygame.draw.circle(screen, (200, 200, 200), (int(end_x), int(end_y)), 2)

    def _cast_sensor(self, track_mask, relative_angle):
        angle = math.radians(self.angle + relative_angle)
        for dist in range(SENSOR_LENGTH):
            target_x = int(self.x + dist * math.cos(angle))
            target_y = int(self.y - dist * math.sin(angle))

            if target_x < 0 or target_y < 0 or target_x >= track_mask.get_width() or target_y >= track_mask.get_height():
                break

            color = track_mask.get_at((target_x, target_y))
            if color != (0, 0, 0, 255):
                return dist, target_x, target_y

        return SENSOR_LENGTH, target_x, target_y

    def _check_collision(self, track_mask):
        color = track_mask.get_at((int(self.x), int(self.y)))
        return color != (0, 0, 0, 255)

    def get_sensor_data(self):
        return np.array([s[1] for s in self.sensors])
