import pygame
from tile import StaticTile
from projectile import Projectile
from settings import screen_width
import random

class Enemy(StaticTile):
    def __init__(self,size,x,y, image = None):
        super().__init__(size,x,y, image)
        self.projectiles = pygame.sprite.Group()   
        self.x = x
        self.y = y    
        self.facing_right = False
        self.shoot_cooldown = 0
        self.randnum = random.randint(1,10)

    def shoot_projectile(self): #method for the shoot projectile
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.randnum * 100
            projectile = Projectile(self.rect.x, self.rect.y, self.facing_right) #makes projectile object from the position of the player. 
            self.projectiles.add(projectile) 

    def update(self, shift):
        self.rect.x += shift
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1



class Red_Monster(Enemy):
    def __init__(self,size,x,y):
        super().__init__(size,x,y, pygame.image.load('../graphics/enemies/red_monster/red_monster_single.png').convert_alpha())

    def update(self, shift):
        super().update(shift)

class Wasp(Enemy):
    def __init__(self,size,x,y):
        super().__init__(size,x,y, pygame.image.load('../graphics/enemies/wasp/wasp1.png').convert_alpha())

    def update(self, shift):
        super().update(shift)    

class Queen_Wasp(Enemy):
    def __init__(self,size,x,y):
        super().__init__(size,x,y, pygame.image.load('../graphics/enemies/wasp_queen/wasp_queen1.png').convert_alpha())
        self.health = 10
        self.randnum = 1

    def update(self, shift):
        super().update(shift)

        if self.health <= 0:
            self.kill()

