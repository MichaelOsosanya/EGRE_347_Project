import pygame
from tiles import StaticTile
from projectile import Projectile

class Enemy(StaticTile):
    def __init__(self,size,x,y):  #added direction
        super().__init__(size,x,y, pygame.image.load('../graphics/enemies/red_monster_single.png').convert_alpha())
        self.projectiles = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()  #pygames built in function for time in ms
        self.shoot_interval = 5000  # 5000 ms = 5 s
        self.direction = pygame.math.Vector2(-1,0)

    def update(self,shift):
        self.rect.x += shift
        #self.update_shooting
        
    
    """
    def update_shooting(self): 
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.shoot_projectile() 
            self.last_shot_time = current_time
    """

    #below is the def shoot projectile
    def shoot_projectile(self): #method for the shoot projectile
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            #self.shoot_projectile() 
            
            projectile = Projectile(self.rect.x, self.rect.y, self.direction.x) #makes projectile object from the position of the player. 
            self.projectiles.add(projectile)    #adds that projectile to a group
            self.last_shot_time = current_time

    #below is the updated one where it uses the shot interval
    #it was recomeneded to use a timer
    #https://stackoverflow.com/questions/58224668/how-do-i-continuously-trigger-an-action-at-certain-time-intervals-enemy-shoots#:~:text=I%20recommend%20to%20use%20a%20timer%20event.%20Use,bullet_event%20%3D%20pygame.USEREVENT%20%2B%201%20pygame.time.set_timer%20%28bullet_event%2C%20milliseconds_delay%29
    
    """
    def shoot_projectile(self, current_time):
        if current_time - self.last_shot_time > self.shoot_interval:
            projectile = Projectile(self.rect.x, self.rect.y, self.direction.x)
            self.projectiles.add(projectile)
            self.last_shot_time = current_time

    """