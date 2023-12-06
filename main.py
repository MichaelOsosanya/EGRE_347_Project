import pygame, sys
from settings import *
from level import Level, collision_count
from game_data import sky_island

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(sky_island, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    level.run()

    pygame.display.update()
    clock.tick(60)
    print(f"Player Collision Count: {collision_count}")

    
