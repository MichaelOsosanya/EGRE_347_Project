import pygame
from support import import_folder
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.idle[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.shoot_cooldown = 0
        self.max_health = 100
        self.current_health = 100
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0    #changed to 0 so it could "float"
        self.jump_speed = -16

        #player status
        self.facing_right = True
        self.projectiles = pygame.sprite.Group()  # creating an object of the sprite group for the projectile


    def import_character_assets(self):
        character_path = '../graphics/player/robot'

        self.idle = import_folder(character_path)

    def animate(self):
        animation = self.idle

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.shoot_projectile()
 

        if keys[pygame.K_UP]:
            self.direction.y = -8
        elif keys[pygame.K_DOWN]:
            self.direction.y = 8    #so its moving rather slowly going up and down so i changed this mnumber but i think we should try not having gravity for the main player
        else: 
            self.direction.y = 0

            
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def shoot_projectile(self): #method for the shoot projectile
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 15
            projectile = Projectile(self.rect.x, self.rect.y, self.facing_right) #makes projectile object from the position of the player. 
            self.projectiles.add(projectile)    #adds that projectile to a group

    def update(self):
        self.get_input()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1




