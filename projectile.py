
import pygame
from settings import screen_width

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x,y, direction):
        super().__init__()
        
        self.image = pygame.image.load("../graphics/orb.png").convert()  # Load the projectile image
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL) #using the jet tutroial in class i made the orb as an image
        self.image = pygame.transform.scale(self.image,(32,32)) #scaled it so it didn't take up half the screen
        self.rect = self.image.get_rect(center=(x, y)) #create an rectangluar objecct the shows the position, should be changed to a circular one
        self.speed = 8
        self.direction = direction      


    def update(self):
        #updates coordinates based on speed and direction. direction is set by placing facing
        
        self.rect.x += self.speed * self.direction
        if self.rect.right <0 or self.rect.left > screen_width:
            self.kill()

  
