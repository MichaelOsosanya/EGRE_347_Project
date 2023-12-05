import pygame
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32,64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0    #changed to 0 so it could "float"
        self.jump_speed = -16

        self.projectiles = pygame.sprite.Group()  # creating an object of the sprite group for the projectile

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -8
        elif keys[pygame.K_DOWN]:
            self.direction.y = 8    #so its moving rather slowly going up and down so i changed this mnumber but i think we should try not having gravity for the main player
        else: 
            self.direction.y = 0

            


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def update(self):
        self.get_input()

