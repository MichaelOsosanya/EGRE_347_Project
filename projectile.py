
import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x,y, direction):
        super().__init__()
        
        self.image = pygame.image.load("orb.png").convert()  # Load the projectile image
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL) #using the jet tutroial in class i made the orb as an image
        self.image = pygame.transform.scale(self.image,(32,32)) #scaled it so it didn't take up half the screen
        self.rect = self.image.get_rect(center=(x, y)) #create an rectangluar objecct the shows the position, should be changed to a circular one
        self.speed = 12
        self.direction = direction      


    def update(self):
        #updates coordinates based on speed and direction. direction is set by placing facing
        self.rect.x += self.speed * self.direction
        
        """
        # possible collision code for hitting tiles, still needs to be worked out
        collisions = pygame.sprite.spritecollide(self, self.level.tiles, False)
        for tile in collisions:
            
            self.kill()
            """
        

        