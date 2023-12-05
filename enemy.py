import pygame
from tiles import StaticTile

class Enemy(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y, pygame.image.load('../graphics/enemies/red_monster_single.png').convert_alpha())
    

    def update(self,shift):
        self.rect.x += shift

