import pygame
from tiles import StaticTile, Tile
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width
from player import Player
from enemy import Enemy

class Level:
    def __init__(self, level_data, surface): 

        #level setup
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  #adding this made it possible for the level to actually render the object on the screen. i tried doing this in the main but i found it easier to have the level design render this
        self.display_surface = surface

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        #terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies') 



    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain_tiles2.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if val == '5':
                        sprite = Player((x,y), self.display_surface)
                        self.player.add(sprite)

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
        collidable_sprites =  self.terrain_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites =  self.terrain_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def projectile_tile_collide(self):    #adding method for detectile collision for projectiles with tiles
        for projectile in self.projectiles.sprites():
            projectile.rect.x += projectile.speed * projectile.direction
            collidable_sprites =  self.terrain_sprites.sprites()
        
            for sprite in collidable_sprites:
                if projectile.rect.colliderect(sprite.rect):
                    projectile.kill()     #using kill method to remove projectile

    def run(self):
        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #enemy
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_sprites.update(self.world_shift)

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)

        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)


        self.projectiles.update()  #updates the projecciles position and speed
        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()
