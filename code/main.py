import pygame, sys
from settings import *
from level import Level
from game_data import sky_island
from UI import UI
from player import Player
#from level import collision_count

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level( sky_island,screen)
ui = UI(screen)
collisionCount = level.collision_count

while True:
    # update and draw sprites
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    #player.health_bar.draw(screen)
    level.run()
    #print ("Collsion count is: ", level.collision_count)
    damage_taken = level.collision_count * 10  #player damage is 10
    current_health = 100 - damage_taken      #player health is 100
   # print("current_health is ", current_health)
    ui.show_health(current_health,100)
    pygame.display.update()
    clock.tick(60)
