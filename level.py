import pygame
import button
from tile import StaticTile, Tile, Blue_Portal, Text
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width, screen_height
from player import Player
from enemy import Red_Monster, Wasp, Queen_Wasp, Kraken, Hollow


class Tutorial:
    def __init__(self, level_data, surface, game_state): 

        self.collision_count = 0
        self.game_state = game_state

        #level setup
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  #adding this made it possible for the level to actually render the object on the screen. i tried doing this in the main but i found it easier to have the level design render this
        self.display_surface = surface
        self.player_layout = import_csv_layout(level_data['player'])
        self.terrain_layout = import_csv_layout(level_data['terrain'])
        self.portal_layout = import_csv_layout(level_data['portal'])
        self.background_layout = import_csv_layout(level_data['background'])
        self.text1_layout = import_csv_layout(level_data['text1'])
        self.text2_layout = import_csv_layout(level_data['text2'])
        self.text3_layout = import_csv_layout(level_data['text3'])
        self.text4_layout = import_csv_layout(level_data['text4'])
        self.text5_layout = import_csv_layout(level_data['text5'])
      
        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #text
        self.text1_sprites = self.create_tile_group(self.text1_layout, 'text1')
        self.text2_sprites = self.create_tile_group(self.text2_layout, 'text2')
        self.text3_sprites = self.create_tile_group(self.text3_layout, 'text3')
        self.text4_sprites = self.create_tile_group(self.text4_layout, 'text4')
        self.text5_sprites = self.create_tile_group(self.text5_layout, 'text5')

        #background
        self.background_sprites = self.create_tile_group(self.background_layout, 'background')


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/station_tiles.png')
                        terrain_tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,terrain_tile_surface)

                    elif type == 'background':
                        background_tile_list = import_cut_graphics('../graphics/backgrounds/stars.png')
                        background_tile_surface = background_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,background_tile_surface)

                    elif type == 'text1':
                        sprite = Text(tile_size,x,y,'../graphics/backgrounds/TEXT1.png')

                    elif type == 'text2':
                        sprite = Text(tile_size,x,y,'../graphics/backgrounds/TEXT2.png')

                    elif type == 'text3':
                        sprite = Text(tile_size,x,y,'../graphics/backgrounds/TEXT3.png')

                    elif type == 'text4':
                        sprite = Text(tile_size,x,y,'../graphics/backgrounds/TEXT4.png') 

                    elif type == 'text5':
                        sprite = Text(tile_size,x,y,'../graphics/backgrounds/TEXT5.png')   

                    elif type == 'portal':
                        sprite = Blue_Portal(tile_size,x,y)

                    else:
                        continue
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    self.player_spawn_x  = col_index * tile_size
                    self.player_spawn_y = row_index * tile_size
                    if val == '0':
                        sprite = Player(self.player_spawn_x ,self.player_spawn_y, self.display_surface)
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

  
    def open_try_again_menu(self):
        self.game_state.game_paused = True
        if self.game_state.level_state == "Tutorial":
            self.game_state.state = "try_again_menu"

    def open_next_menu(self):
         
        self.game_state.game_paused = True       
        if self.game_state.level_state == "Tutorial":
            self.game_state.state = "next_menu"

    def check_death(self):
        if self.player.sprite.rect.top < 0 or self.player.sprite.rect.top > screen_height or self.player.sprite.current_health <= 0:
            self.open_try_again_menu()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.portal_sprites, False):
            self.open_next_menu()
    
    def restart(self):
        self.world_shift = 0

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #background
        self.background_sprites = self.create_tile_group(self.background_layout, 'background') 

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #text
        self.text1_sprites = self.create_tile_group(self.text1_layout, 'text1')
        self.text2_sprites = self.create_tile_group(self.text2_layout, 'text2')
        self.text3_sprites = self.create_tile_group(self.text3_layout, 'text3')
        self.text4_sprites = self.create_tile_group(self.text4_layout, 'text4')
        self.text5_sprites = self.create_tile_group(self.text5_layout, 'text5')

    def run(self):
    
        current_time = pygame.time.get_ticks()  #added a tick timer

        #Background
        self.background_sprites.draw(self.display_surface)
        self.background_sprites.update(self.world_shift)


        #portal
        self.portal_sprites.draw(self.display_surface)
        self.portal_sprites.update(self.world_shift)


        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #text
        self.text1_sprites.draw(self.display_surface)
        self.text1_sprites.update(self.world_shift)
        self.text2_sprites.draw(self.display_surface)
        self.text2_sprites.update(self.world_shift)
        self.text3_sprites.draw(self.display_surface)
        self.text3_sprites.update(self.world_shift)
        self.text4_sprites.draw(self.display_surface)
        self.text4_sprites.update(self.world_shift)
        self.text5_sprites.draw(self.display_surface)
        self.text5_sprites.update(self.world_shift)

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.check_death()
        self.check_win()



        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)

        self.projectiles.update()  #updates the projectiles position and speed
    
        for projectile in self.projectiles.sprites():
            projectile.rect.x += self.world_shift

        self.projectile_tile_collide()

        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()

class Sky_Island_Level:
    def __init__(self, level_data, surface, game_state): 

        self.collision_count = 0
        self.game_state = game_state
        #level setup
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  #adding this made it possible for the level to actually render the object on the screen. i tried doing this in the main but i found it easier to have the level design render this
        self.display_surface = surface
        self.player_layout = import_csv_layout(level_data['player'])
        self.terrain_layout = import_csv_layout(level_data['terrain'])
        self.portal_layout = import_csv_layout(level_data['portal'])
        self.monster_layout = import_csv_layout(level_data['monsters'])
      
        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #red monsters
        self.monster_sprites = self.create_tile_group(self.monster_layout, 'monsters') 


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
                    
                    elif type == 'portal':
                        sprite = Blue_Portal(tile_size,x,y)

                    elif type == 'monsters':
                        sprite = Red_Monster(tile_size,x,y)

                    else:
                        continue
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    self.player_spawn_x  = col_index * tile_size
                    self.player_spawn_y = row_index * tile_size
                    if val == '0':
                        sprite = Player(self.player_spawn_x ,self.player_spawn_y, self.display_surface)
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
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
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
            collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
            for sprite in collidable_sprites:
                if projectile.rect.colliderect(sprite.rect):
                    projectile.kill()     #using kill method to remove projectile


    def monster_shoots_player(self):
        for projectile in self.monster_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.player.sprite.take_damage()
    
    def player_shoots_monster(self):
        for enemy in self.monster_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.kill()

        
    def open_try_again_menu(self):
        self.game_state.game_paused = True
        if self.game_state.level_state == "Sky_Island":
            self.game_state.state = "try_again_menu"

    def open_next_menu(self):
         
        self.game_state.game_paused = True       
        if self.game_state.level_state == "Sky_Island":
            self.game_state.state = "next_menu"

    def check_death(self):
        if self.player.sprite.rect.top < 0 or self.player.sprite.rect.top > screen_height or self.player.sprite.current_health <= 0:
            self.open_try_again_menu()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.portal_sprites, False):
            self.open_next_menu()
    
    def restart(self):
        self.world_shift = 0

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #red monsters
        self.monster_sprites = self.create_tile_group(self.monster_layout, 'monsters') 


    def run(self):
    
        current_time = pygame.time.get_ticks()  #added a tick timer

        #Sky Background
        #self.sky_background_sprites.draw(self.display_surface)
        #self.sky_background_sprites.update(self.world_shift)

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #Decoration
        #self.decoration_sprites.draw(self.display_surface)
        #self.decoration_sprites.update(self.world_shift)

        #portal
        self.portal_sprites.draw(self.display_surface)
        self.portal_sprites.update(self.world_shift)

        #red monster
        self.monster_sprites.draw(self.display_surface)
        self.monster_sprites.update(self.world_shift)

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.check_death()
        self.check_win()
        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)

        for enemy in self.monster_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        self.projectiles.update()  #updates the projectiles position and speed
    
        for projectile in self.projectiles.sprites():
            projectile.rect.x += self.world_shift
        
        #self.enemy_shoots_player()
        self.monster_shoots_player()

        #player shoots enemy
        self.player_shoots_monster()

        self.projectile_tile_collide()

        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()

class Hive_Level:
    def __init__(self, level_data, surface, game_state): 

        self.collision_count = 0
        self.current_level = 1
        self.game_state = game_state
        #level setup
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  
        self.display_surface = surface
        self.player_layout = import_csv_layout(level_data['player'])
        self.honeycomb_layout = import_csv_layout(level_data['honeycomb'])
        self.wasp_queen_layout = import_csv_layout(level_data['wasp_queen'])
        self.portal_layout = import_csv_layout(level_data['portal'])
        self.wasp_layout = import_csv_layout(level_data['wasp'])

        #player 
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #honeycomb
        self.honeycomb_sprites = self.create_tile_group(self.honeycomb_layout, 'honeycomb')

        #wasp queen
        self.wasp_queen_sprites = self.create_tile_group(self.wasp_queen_layout, 'wasp_queen')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #wasp
        self.wasp_sprites = self.create_tile_group(self.wasp_layout, 'wasp') 


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'honeycomb':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/honeycomb.png')
                        terrain_tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,terrain_tile_surface)
                    
                    elif type == 'portal':
                        sprite = Blue_Portal(tile_size,x,y)

                    elif type == 'wasp':
                        sprite = Wasp(tile_size,x,y)

                    elif type == 'wasp_queen':
                        sprite = Queen_Wasp(tile_size,x,y)
                    else:
                        continue
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if val == '0':
                        sprite = Player(x,y, self.display_surface)
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
        collidable_sprites =  self.honeycomb_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.honeycomb_sprites.sprites()
        
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
            collidable_sprites =  self.honeycomb_sprites.sprites()
        
            for sprite in collidable_sprites:
                if projectile.rect.colliderect(sprite.rect):
                    projectile.kill()     #using kill method to remove projectile
    
    def wasp_shoots_player(self):
        for projectile in self.wasp_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.player.sprite.take_damage()

    def queen_wasp_shoots_player(self):
        for projectile in self.wasp_queen_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.player.sprite.take_damage()

    def player_shoots_wasp(self):
        for enemy in self.wasp_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.kill()

    def player_shoots_queen_wasp(self):
        for enemy in self.wasp_queen_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.health -= 1

    def open_try_again_menu(self):
        self.game_state.game_paused = True
        if self.game_state.level_state == "Hive":
            self.game_state.state = "try_again_menu"

    def open_next_menu(self):
        self.game_state.game_paused = True       
        if self.game_state.level_state == "Hive":
            self.game_state.state = "next_menu"

    def check_death(self):
        if self.player.sprite.rect.top < 0 or self.player.sprite.rect.top > screen_height or self.player.sprite.current_health <= 0:
            self.open_try_again_menu()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.portal_sprites, False):
            self.open_next_menu()
    
    def restart(self):
        self.world_shift = 0

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.honeycomb_sprites = self.create_tile_group(self.honeycomb_layout, 'honeycomb')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #wasp queen
        self.wasp_queen_sprites = self.create_tile_group(self.wasp_queen_layout, 'wasp_queen')

        #wasp
        self.wasp_sprites = self.create_tile_group(self.wasp_layout, 'wasp')


    def run(self): 
        current_time = pygame.time.get_ticks()  #added a tick timer

        #Honeycomb Background
        #self.honeycomb_background_sprites.draw(self.display_surface)
        #self.honeycomb_background_sprites.update(self.world_shift)

        #honeycomb
        self.honeycomb_sprites.draw(self.display_surface)
        self.honeycomb_sprites.update(self.world_shift)

        #portal
        self.portal_sprites.draw(self.display_surface)
        self.portal_sprites.update(self.world_shift)

        #wasp
        self.wasp_sprites.draw(self.display_surface)
        self.wasp_sprites.update(self.world_shift)

        #queen wasp
        self.wasp_queen_sprites.draw(self.display_surface)
        self.wasp_queen_sprites.update(self.world_shift)    
    
        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.check_death()
        self.check_win()

        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)

        for enemy in self.wasp_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        for enemy in self.wasp_queen_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        self.projectiles.update()  #updates the projectiles position and speed
    
        for projectile in self.projectiles.sprites():
            projectile.rect.x += self.world_shift
                
        self.wasp_shoots_player()
        self.queen_wasp_shoots_player()
        self.player_shoots_wasp()
        self.player_shoots_queen_wasp()
        
        self.projectile_tile_collide()

        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()


class Ocean_Depths1:
    def __init__(self, level_data, surface, game_state): 

        self.collision_count = 0
        self.game_state = game_state

        #level setup
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  #adding this made it possible for the level to actually render the object on the screen. i tried doing this in the main but i found it easier to have the level design render this
        self.display_surface = surface
        self.player_layout = import_csv_layout(level_data['player'])
        self.terrain_layout = import_csv_layout(level_data['terrain'])
        self.portal_layout = import_csv_layout(level_data['portal'])
        self.monster_layout = import_csv_layout(level_data['monsters'])
      
        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #red monsters
        self.monster_sprites = self.create_tile_group(self.monster_layout, 'monsters') 


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/ocean_tiles.png')
                        terrain_tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,terrain_tile_surface)
                    
                    elif type == 'portal':
                        sprite = Blue_Portal(tile_size,x,y)

                    elif type == 'monsters':
                        sprite = Red_Monster(tile_size,x,y)

                    else:
                        continue
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    self.player_spawn_x  = col_index * tile_size
                    self.player_spawn_y = row_index * tile_size
                    if val == '0':
                        sprite = Player(self.player_spawn_x ,self.player_spawn_y, self.display_surface)
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
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
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
            collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
            for sprite in collidable_sprites:
                if projectile.rect.colliderect(sprite.rect):
                    projectile.kill()     #using kill method to remove projectile


    def monster_shoots_player(self):
        for projectile in self.monster_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.player.sprite.take_damage()
    
    def player_shoots_monster(self):
        for enemy in self.monster_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.kill()
 
    def open_try_again_menu(self):
        self.game_state.game_paused = True
        if self.game_state.level_state == "Ocean_Depths1":
            self.game_state.state = "try_again_menu"

    def open_next_menu(self):
         
        self.game_state.game_paused = True       
        if self.game_state.level_state == "Ocean_Depths1":
            self.game_state.state = "next_menu"

    def check_death(self):
        if self.player.sprite.rect.top < 0 or self.player.sprite.rect.top > screen_height or self.player.sprite.current_health <= 0:
            self.open_try_again_menu()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.portal_sprites, False):
            self.open_next_menu()
    
    def restart(self):
        self.world_shift = 0

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #red monsters
        self.monster_sprites = self.create_tile_group(self.monster_layout, 'monsters') 


    def run(self):
    
        current_time = pygame.time.get_ticks()  #added a tick timer

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #portal
        self.portal_sprites.draw(self.display_surface)
        self.portal_sprites.update(self.world_shift)

        #red monster
        self.monster_sprites.draw(self.display_surface)
        self.monster_sprites.update(self.world_shift)

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.check_death()
        self.check_win()
        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)

        for enemy in self.monster_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        self.projectiles.update()  #updates the projectiles position and speed
    
        for projectile in self.projectiles.sprites():
            projectile.rect.x += self.world_shift
        
        #self.enemy_shoots_player()
        self.monster_shoots_player()

        #player shoots enemy
        self.player_shoots_monster()

        self.projectile_tile_collide()

        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()


class Ocean_Depths2:
    def __init__(self, level_data, surface, game_state): 

        self.collision_count = 0
        self.game_state = game_state

        #level setup
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  #adding this made it possible for the level to actually render the object on the screen. i tried doing this in the main but i found it easier to have the level design render this
        self.display_surface = surface
        self.player_layout = import_csv_layout(level_data['player'])
        self.terrain_layout = import_csv_layout(level_data['terrain'])
        self.portal_layout = import_csv_layout(level_data['portal'])
        self.monster_layout = import_csv_layout(level_data['monsters'])
        self.boss_layout = import_csv_layout(level_data['boss'])

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #red monsters
        self.monster_sprites = self.create_tile_group(self.monster_layout, 'monsters') 

        #boss
        self.boss_sprites = self.create_tile_group(self.boss_layout, 'boss') 

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/ocean_tiles.png')
                        terrain_tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,terrain_tile_surface)
                    
                    elif type == 'portal':
                        sprite = Blue_Portal(tile_size,x,y)

                    elif type == 'monsters':
                        sprite = Red_Monster(tile_size,x,y)
                    elif type == 'boss':
                        sprite = Kraken(tile_size,x,y)
                    else:
                        continue
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    self.player_spawn_x  = col_index * tile_size
                    self.player_spawn_y = row_index * tile_size
                    if val == '0':
                        sprite = Player(self.player_spawn_x ,self.player_spawn_y, self.display_surface)
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
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
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
            collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
            for sprite in collidable_sprites:
                if projectile.rect.colliderect(sprite.rect):
                    projectile.kill()     #using kill method to remove projectile


    def monster_shoots_player(self):
        for projectile in self.monster_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.player.sprite.take_damage()
    
    def player_shoots_monster(self):
        for enemy in self.monster_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.kill()

    def player_shoots_kraken(self):
        for enemy in self.boss_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.health -= 1

    def kraken_shoots_player(self):
        for projectile in self.boss_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.player.sprite.take_damage()

    def open_try_again_menu(self):
        self.game_state.game_paused = True
        if self.game_state.level_state == "Ocean_Depths2":
            self.game_state.state = "try_again_menu"

    def open_next_menu(self):
        
        self.game_state.game_paused = True       
        if self.game_state.level_state == "Ocean_Depths2":
            self.game_state.state = "next_menu"

    def check_death(self):
        if self.player.sprite.rect.top < 0 or self.player.sprite.rect.top > screen_height or self.player.sprite.current_health <= 0:
            self.open_try_again_menu()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.portal_sprites, False):
            self.open_next_menu()
    
    def restart(self):
        self.world_shift = 0

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')

        #portal
        self.portal_sprites = self.create_tile_group(self.portal_layout, 'portal')

        #red monsters
        self.monster_sprites = self.create_tile_group(self.monster_layout, 'monsters') 

        #boss
        self.boss_sprites = self.create_tile_group(self.boss_layout, 'boss') 

    def run(self):
    
        current_time = pygame.time.get_ticks()  #added a tick timer

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        
        #portal
        self.portal_sprites.draw(self.display_surface)
        self.portal_sprites.update(self.world_shift)

        #red monster
        self.monster_sprites.draw(self.display_surface)
        self.monster_sprites.update(self.world_shift)

        #boss
        self.boss_sprites.draw(self.display_surface)
        self.boss_sprites.update(self.world_shift)

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.check_death()
        self.check_win()
        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)

        for enemy in self.monster_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        self.projectiles.update()  #updates the projectiles position and speed
    
        for projectile in self.projectiles.sprites():
            projectile.rect.x += self.world_shift
        
        #self.enemy_shoots_player()
        self.monster_shoots_player()

        #player shoots enemy
        self.player_shoots_monster()
        self.player_shoots_kraken()
        self.kraken_shoots_player()
        self.projectile_tile_collide()

        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()
    
class Cave:
    def __init__(self, level_data, surface, game_state): 

        self.collision_count = 0
        self.game_state = game_state

        #level setup
        self.world_shift = 0 #camera starting point
        self.projectiles = pygame.sprite.Group()  #adding this made it possible for the level to actually render the object on the screen. i tried doing this in the main but i found it easier to have the level design render this
        self.display_surface = surface

        self.player_layout = import_csv_layout(level_data['player'])
        self.background_layout = import_csv_layout(level_data['background'])
        self.terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain1_layout = import_csv_layout(level_data['terrain1'])
        self.boss_layout = import_csv_layout(level_data['boss'])

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #self.background_sprites = self.create_tile_group(self.background_layout, 'background')

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')
        self.terrain1_sprites = self.create_tile_group(self.terrain1_layout, 'terrain1')

        #boss
        self.boss_sprites = self.create_tile_group(self.boss_layout, 'boss') 

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/cavern_tiles.png')
                        terrain_tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,terrain_tile_surface)
                    
                    if type == 'terrain1':
                        terrain1_tile_list = import_cut_graphics('../graphics/terrain/cave_tiles.png')
                        terrain1_tile_surface = terrain1_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,terrain1_tile_surface)

                    
                    #if type == 'background':
                        #background_tile_list = import_cut_graphics('../graphics/terrain/cave_background.png')
                        #background_tile_surface = background_tile_list[int(val)]
                        #sprite = StaticTile(tile_size,x,y,background_tile_surface)

                    elif type == 'boss':
                        sprite = Hollow(tile_size,x,y, self)
                    else:
                        continue
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                    self.player_spawn_x  = col_index * tile_size
                    self.player_spawn_y = row_index * tile_size
                    if val == '0':
                        sprite = Player(self.player_spawn_x ,self.player_spawn_y, self.display_surface)
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
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
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
            collidable_sprites =  self.terrain_sprites.sprites() #+ self.honeycomb_sprites.sprites()
        
            for sprite in collidable_sprites:
                if projectile.rect.colliderect(sprite.rect):
                    projectile.kill()     #using kill method to remove projectile

    def player_shoots_hollow(self):
        for enemy in self.boss_sprites.sprites():
            enemy_collisions = pygame.sprite.spritecollide(enemy, self.player.sprite.projectiles, True)
            if enemy_collisions:
                enemy.health -= 1

    def hollow_shoots_player(self):
        for projectile in self.boss_sprites.sprites():
            projectile_collisions = pygame.sprite.spritecollide(self.player.sprite, projectile.projectiles, True)
            if projectile_collisions:
                self.player.sprite.take_damage()

    def open_try_again_menu(self):
        self.game_state.game_paused = True
        if self.game_state.level_state == "The_Cave":
            self.game_state.state = "try_again_menu"

    def open_next_menu(self):
        self.game_state.game_paused = True
        if self.game_state.level_state == "The_Cave":
            self.game_state.state = "game_won"

    def check_death(self):
        if self.player.sprite.rect.top < 0 or self.player.sprite.rect.top > screen_height or self.player.sprite.current_health <= 0:
            self.open_try_again_menu()

    def check_win(self):
        pass

    def restart(self):
        self.world_shift = 0

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(self.player_layout)

        #self.background_sprites = self.create_tile_group(self.background_layout, 'background')

        #terrain
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')
        self.terrain1_sprites = self.create_tile_group(self.terrain1_layout, 'terrain1')

        #boss
        self.boss_sprites = self.create_tile_group(self.boss_layout, 'boss') 

    def run(self):
    
        current_time = pygame.time.get_ticks()  #added a tick timer

        #background
        #self.boss_sprites.draw(self.display_surface)
        #self.boss_sprites.update(self.world_shift)

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        self.terrain1_sprites.draw(self.display_surface)
        self.terrain1_sprites.update(self.world_shift)

        #boss
        self.boss_sprites.draw(self.display_surface)
        self.boss_sprites.update(self.world_shift)

        #player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.check_death()

        for projectile in self.player.sprite.projectiles:   #if the projecile is made its gets added to the group created above here 
            self.projectiles.add(projectile)

        for enemy in self.boss_sprites.sprites():   #added a loop for enemy projectiles
            enemy.shoot_projectile()
            for projectile in enemy.projectiles:
                self.projectiles.add(projectile)

        self.projectiles.update()  #updates the projectiles position and speed
    
        for projectile in self.projectiles.sprites():
            projectile.rect.x += self.world_shift
    

        #player shoots enemy
        self.player_shoots_hollow()
        self.hollow_shoots_player()
        self.projectile_tile_collide()

        self.projectiles.draw(self.display_surface)  #is whats actually rendering the object 

        self.projectile_tile_collide()   #calling the method to ensure the projectile removes itself

        pygame.display.flip()