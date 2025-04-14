import pygame
import sys
from agents.car_agent import Car

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Self-Driving Car Simulator")

track_img = pygame.image.load("data/track.png").convert()
track_mask = pygame.mask.from_surface(track_img).to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))

start_x, start_y = 100, 500
car = Car(start_x, start_y)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))  
    screen.blit(track_img, (0, 0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car.update(screen, track_img)

    if car.alive:
        sensor_data = car.get_sensor_data()
        print("Sensores:", sensor_data)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
