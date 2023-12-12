import pygame
import button

pygame.init()

#create game window
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
tutorial_img = pygame.image.load("images/tutorial.png").convert_alpha()
level_one_img = pygame.image.load("images/level_one.png").convert_alpha()
level_two_img = pygame.image.load("images/level_two.png").convert_alpha()
level_three_img = pygame.image.load("images/level_three.png").convert_alpha()
main_menu_img = pygame.image.load("images/main_menu.png").convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()
#video_img = pygame.image.load('images/button_video.png').convert_alpha()
#audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
#keys_img = pygame.image.load('images/button_keys.png').convert_alpha()

#create button instances
options_button = button.Button(390, 600, options_img, 1)
quit_button = button.Button(740, 600, quit_img, 1)
tutorial_button = button.Button(30, 600, tutorial_img, 1) #double chack values
level_one_button = button.Button(20, 100, level_one_img, 1)
level_two_button = button.Button(350, 100, level_two_img, 1)
level_three_button = button.Button(750, 100, level_three_img, 1)
main_menu_button = button.Button(380, 200, main_menu_img, 1)
resume_button = button.Button(380, 500, resume_img, 1)
quit_button_two = button.Button(380, 800, quit_img, 1)

#back_button = button.Button(332, 600, back_img, 1)
# resume_button = button.Button(304, 125, resume_img, 1)
# options_button = button.Button(297, 250, options_img, 1)
# quit_button = button.Button(336, 375, quit_img, 1)
# tutorial_button = button.Button(336, 375, tutorial_img, 1) #double chack values
# level_one_button = button.Button(226, 75, level_one_img, 1)
# level_two_button = button.Button(225, 200, level_two_img, 1)
# level_three_button = button.Button(246, 325, level_three_img, 1)
# main_menu_button = button.Button(246, 325, main_menu_img, 1)
#video_button = button.Button(226, 75, video_img, 1)
#audio_button = button.Button(225, 200, audio_img, 1)
#keys_button = button.Button(246, 325, keys_img, 1)


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
while run:

  screen.fill((52, 78, 91))

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if tutorial_button.draw(screen):
        print("Tutorial")
      if level_one_button.draw(screen):
        print("Level 1")
      if level_two_button.draw(screen):
        print("Level 2")
      if level_three_button.draw(screen):
        print("Level 3")
      if options_button.draw(screen):
        print("Options")
        menu_state = "options"
      if quit_button.draw(screen):
        run = False
        #menu_state = "main"

    #check if the options menu is open
    if menu_state == "options":
      #draw the different options buttons
      if resume_button.draw(screen):
        game_paused = False
      if main_menu_button.draw(screen):
        menu_state = "Main Menu"
        menu_state = "main"
      if quit_button_two.draw(screen):
        run = False
  else:
    draw_text("Press 'ESCAPE' to pause", font, TEXT_COL, 350, 350)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()