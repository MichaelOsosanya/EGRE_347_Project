import pygame
from tile import StaticTile, Tile
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width
from player import Player
from enemy import Red_Monster, Wasp, Queen_Wasp

class Level:
    def __init__(self, level_data, surface): 

        self.collision_count = 0

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

        #Sky Background
        sky_background_layout = import_csv_layout(level_data['sky_background'])
        self.sky_background_sprites = self.create_tile_group(sky_background_layout, 'sky_background')

        #Decoration
        decoration_layout = import_csv_layout(level_data['decoration'])
        self.decoration_sprites = self.create_tile_group(decoration_layout, 'decoration')

        #red monsters
        monster_layout = import_csv_layout(level_data['monsters'])
        self.monster_sprites = self.create_tile_group(monster_layout, 'monsters') 

        #honeycomb
        honeycomb_layout = import_csv_layout(level_data['honeycomb'])
        self.honeycomb_sprites = self.create_tile_group(honeycomb_layout, 'honeycomb')

        #honeycomb background
        honeycomb_background_layout = import_csv_layout(level_data['honeycomb_background'])
        self.honeycomb_background_sprites = self.create_tile_group(honeycomb_background_layout, 'honeycomb_background')

        #wasps
        wasp_layout = import_csv_layout(level_data['wasp'])
        self.wasp_sprites = self.create_tile_group(wasp_layout, 'wasp') 

        #queen wasp
        queen_wasp_layout = import_csv_layout(level_data['queen_wasp'])
        self.queen_wasp_sprites = self.create_tile_group(queen_wasp_layout, 'queen_wasp') 

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles2.png')
                        terrain_tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,terrain_tile_surface)

                    elif type == 'honeycomb':
                        honeycomb_tile_list = import_cut_graphics('../graphics/terrain/honeycomb.png')
                        honeycomb_tile_surface = honeycomb_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,honeycomb_tile_surface)

                    elif type == 'monsters':
                        sprite = Red_Monster(tile_size,x,y)

                    elif type == 'wasp':
                        sprite = Wasp(tile_size,x,y)

                    elif type == 'queen_wasp':
                        sprite = Queen_Wasp(tile_size,x,y)  

                    elif type == 'honeycomb_background':
                        honeycomb_background_tile_list = import_cut_graphics('../graphics/terrain/honeycomb.png')
                        #print("val:", val)
                        #print("len(honeycomb_background_tile_list):", len(honeycomb_background_tile_list))
                        honeycomb_background_tile_surface = honeycomb_background_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,honeycomb_background_tile_surface)

                    elif type == 'sky_background':
                        sky_background_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles2.png')
                        sky_background_tile_surface = sky_background_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,sky_background_tile_surface) 

                    elif type == 'decoration':
                        decoration_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles2.png')
                        decoration_tile_surface = decoration_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,decoration_tile_surface)
                    else:
                        continue
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if val == '3':
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
        collidable_sprites =  self.terrain_sprites.sprites() + self.honeycomb_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites =  self.terrain_sprites.sprites() + self.honeycomb_sprites.sprites()
        
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
            collidable_sprites =  self.terrain_sprites.sprites() + self.honeycomb_sprites.sprites()
        
            for sprite in collidable_sprites:
                if projectile.rect.colliderect(sprite.rect):
                    projectile.kill()     #using kill method to remove projectile


    def monster_shoots_player(self):
        for projectile in self.monster_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.collision_count += 1
                print(f"Player Collision Count: {self.collision_count}")

    def wasp_shoots_player(self):
        for projectile in self.wasp_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.collision_count += 1
                print(f"Player Collision Count: {self.collision_count}")

    def queen_wasp_shoots_player(self):
        for projectile in self.queen_wasp_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.collision_count += 1
                print(f"Player Collision Count: {self.collision_count}")

    def player_shoots_monster(self):
        for enemy in self.monster_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.kill()
    
    def player_shoots_wasp(self):
        for enemy in self.wasp_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.kill()

    def player_shoots_queen_wasp(self):
        for enemy in self.queen_wasp_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.health -= 1

    def run(self):
    
        current_time = pygame.time.get_ticks()  #added a tick timer

        #Sky Background
        self.sky_background_sprites.draw(self.display_surface)
        self.sky_background_sprites.update(self.world_shift)

        #Honeycomb Background
        self.honeycomb_background_sprites.draw(self.display_surface)
        self.honeycomb_background_sprites.update(self.world_shift)

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #honeycomb
        self.honeycomb_sprites.draw(self.display_surface)
        self.honeycomb_sprites.update(self.world_shift)

        #Decoration
        self.decoration_sprites.draw(self.display_surface)
        self.decoration_sprites.update(self.world_shift)

        #red monster
        self.monster_sprites.draw(self.display_surface)
        self.monster_sprites.update(self.world_shift)

        #wasp
        self.wasp_sprites.draw(self.display_surface)
        self.wasp_sprites.update(self.world_shift)

        #queen wasp
        self.queen_wasp_sprites.draw(self.display_surface)
        self.queen_wasp_sprites.update(self.world_shift)    
    
        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)

        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)

        for enemy in self.monster_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        for enemy in self.wasp_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        for enemy in self.queen_wasp_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        self.projectiles.update()  #updates the projecciles position and speed
    
        for projectile in self.projectiles.sprites():
            projectile.rect.x += self.world_shift
        
        #self.enemy_shoots_player()
        self.monster_shoots_player()
        self.wasp_shoots_player()
        self.queen_wasp_shoots_player()

        #player shoots enemy
        self.player_shoots_monster()
        self.player_shoots_wasp()
        self.player_shoots_queen_wasp()


        self.projectile_tile_collide()

        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()
