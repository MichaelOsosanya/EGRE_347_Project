import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player

class Level:
    def __init__(self, level_data, surface): 

        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  #adding this made it possible for the level to actually render the object on the screen. i tried doing this in the main but i found it easier to have the level design render this

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x,y)) 
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width - screen_width / 2) and direction_x > 0:    #changed divisor by 2 so that he would stay in the first quarter of the screen
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        #level tiles
        self.tiles.update(self.world_shift) #moves camera
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)


        self.projectiles.update()  #updates the projecciles position and speed
        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 


        pygame.display.flip()