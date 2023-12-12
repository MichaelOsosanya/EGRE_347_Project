import pygame, sys
from settings import *
from level import Tutorial, Sky_Island_Level, Hive_Level, Ocean_Depths1, Ocean_Depths2, Cave
from game_data import level_list
import button

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

TEXT_COL = (255, 255, 255)

#load button images
resume_img = pygame.image.load("../graphics/button/button_resume.png").convert_alpha()
options_img = pygame.image.load("../graphics/button/button_options.png").convert_alpha()
quit_img = pygame.image.load("../graphics/button/button_quit.png").convert_alpha()
video_img = pygame.image.load('../graphics/button/button_video.png').convert_alpha()
audio_img = pygame.image.load('../graphics/button/button_audio.png').convert_alpha()
keys_img = pygame.image.load('../graphics/button/button_keys.png').convert_alpha()
back_img = pygame.image.load('../graphics/button/button_back.png').convert_alpha()
exit_img = pygame.image.load('../graphics/button/exit_btn.png').convert_alpha()
start_img = pygame.image.load('../graphics/button/start_btn.png').convert_alpha()
try_again_img = pygame.image.load('../graphics/button/button_try_again.png').convert_alpha()
next_img = pygame.image.load('../graphics/button/button_next.png').convert_alpha()


#create button instances
exit_button = button.Button(405, 350, exit_img, 1)
start_button = button.Button(405, 125, start_img, 1)
resume_button = button.Button(405, 125, resume_img, 1)
options_button = button.Button(405, 250, options_img, 1)
quit_button = button.Button(405, 375, quit_img, 1)
video_button = button.Button(405, 75, video_img, 1)
audio_button = button.Button(405, 200, audio_img, 1)
keys_button = button.Button(405, 325, keys_img, 1)
back_button = button.Button(405, 450, back_img, 1)
try_again_button = button.Button(405, 450, try_again_img, 1)
next_button = button.Button(405, 125, next_img, 1)

class Game_State():
    def __init__(self):
        self.state = "start_menu"
        self.game_paused = True
        self.level_state = "None"
        self.next_level = "None" 
        self.current_level = None
        run = True

    def start_menu(self):
        global run
        if start_button.draw(screen):
            self.game_paused = False
        if exit_button.draw(screen):
            run = False 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "pause_menu"
                    self.game_paused = True
            if event.type == pygame.QUIT:
                run = False

    def try_again_menu(self):
        global run
        if try_again_button.draw(screen):
            self.game_paused = False
            self.current_level.restart()            
        if quit_button.draw(screen):
            run = False

    def options_menu(self):
        global run
        #draw the different options buttons
        if video_button.draw(screen):
            print("Video Settings")
        if audio_button.draw(screen):
            print("Audio Settings")
        if keys_button.draw(screen):
            print("Change Key Bindings")
        if back_button.draw(screen):
            self.state = "pause_menu"

    def pause_menu(self):
        global run
       #draw pause screen buttons
        if resume_button.draw(screen):
            self.game_paused = False
    
        if options_button.draw(screen):
            self.state = "options_menu"
        if quit_button.draw(screen):
            run = False

    def next_menu(self):
        global run
        global level
        draw_text(self.next_level, font, TEXT_COL, 160, 250)
        if next_button.draw(screen):
            self.game_paused = False  

            if self.level_state == "Tutorial":
                self.level_state = "Sky_Island"

            elif self.level_state == "Sky_Island":
                self.level_state = "Hive"

            elif self.level_state == "Hive":
                self.level_state = "Ocean_Depths1"

            elif self.level_state == "Ocean_Depths1":
                self.level_state = "Ocean_Depths2"   

            elif self.level_state == "Ocean_Depths2":                
                self.level_state = "The_Cave"        

            self.load_level()
        
        if exit_button.draw(screen):
                run = False

    def win_menu(self):
        global run
        global level
        draw_text(self.next_level, font, TEXT_COL, 160, 250)
        if exit_button.draw(screen):
            run = False


    def load_level(self):
        if self.level_state == "None":
            self.level_state = "Tutorial"
            self.current_level = Tutorial(level_list[0],screen, game_state)
            self.next_level = "Sky Island"

        elif self.level_state == "Sky_Island":
            self.current_level = Sky_Island_Level(level_list[1],screen, game_state)
            self.next_level = "Hive"

        elif self.level_state == "Hive":
            self.current_level = Hive_Level(level_list[2], screen, game_state)
            self.next_level = "Ocean Depths 1"

        elif self.level_state == "Ocean_Depths1":
            self.current_level = Ocean_Depths1(level_list[3], screen, game_state)
            self.next_level = "Ocean Depths 2"

        elif self.level_state == "Ocean_Depths2":
            self.current_level = Ocean_Depths2(level_list[4], screen, game_state)
            self.next_level = "The Cave"       

        elif self.level_state == "The_Cave":
            self.current_level = Cave(level_list[5], screen, game_state)
            self.next_level = "You won"
            
    def run_level(self):

        if self.level_state == "None":
            self.load_level()
        if not self.game_paused:
            self.state = "unpaused"
  
        screen.fill('grey')
        self.current_level.run()
        self.current_level.check_death()
        self.current_level.check_win()

    def state_manager(self):
        global run
        if self.game_paused == True:
            screen.fill((52, 78, 91))                
            if self.state == "start_menu":
                self.start_menu()
            elif self.state == "try_again_menu":
                self.try_again_menu()
            elif self.state == "pause_menu":
                self.pause_menu()
            elif self.state == "options_menu":
                self.options_menu()
            elif self.state == "next_menu":
                self.next_menu()
            elif self.state == "game_won":
                self.win_menu()                
        else:
            self.run_level()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "pause_menu"
                    self.game_paused = True
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
  
     
pygame.display.set_caption("Main Menu")

#define fonts
font = pygame.font.SysFont("arialblack", 40)

game_state = Game_State()


clock = pygame.time.Clock()
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))


#game loop
run = True

while run:
    game_state.state_manager()
 
    clock.tick(60)

pygame.quit()

