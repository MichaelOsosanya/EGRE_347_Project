import pygame, sys
from settings import *
from level import Level
from game_data import sky_island
from UI import UI
from player import Player

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level( sky_island,screen)
ui = UI(screen)

while True:
    # update and draw sprites
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    #player.health_bar.draw(screen)
    level.run()
    ui.show_health(50,100)
    pygame.display.update()
    clock.tick(60)
