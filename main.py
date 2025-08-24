import pygame
from sys import exit

pygame.init() # Initialize pygame

screen_res = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_res.current_w/2, screen_res.current_h/2
CENTRE_WIDTH = SCREEN_WIDTH // 2
CENTRE_HEIGHT = SCREEN_HEIGHT // 2

game_window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game_title = pygame.display.set_caption("Rock, Paper, Scissor, Revolver")
# Note: once icon made/decided on, add it here. Maybe the idle sprites for the AI
clock = pygame.time.Clock() # Used to cap framerate
ingame_font = pygame.font.Font('assets/fonts/Retro Gaming.ttf',50) # Set font for game

white_bg = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
white_bg.fill("White")

# Get all game assets, and transform and rect appropriately.
# Game title
game_title_surface, game_title_size = pygame.image.load('assets/sprites/other/rpsrevolverlogo.png'), (512/800 * SCREEN_WIDTH,128/450 * SCREEN_HEIGHT) # Get logo image (256x64)
game_title_surface = pygame.transform.scale(game_title_surface, (game_title_size)) # Set size RELATIVE to screen, so it's same regardless of resolution.
game_title_rect = game_title_surface.get_rect()
# Button and text
button_surface, button_size = pygame.image.load('assets/sprites/buttons/buttonflat.png'), (200/800 * SCREEN_WIDTH, 70/450 * SCREEN_HEIGHT)
button_surface = pygame.transform.scale(button_surface, (button_size)) # Set size relative again.
button_rect = button_surface.get_rect()
text_surface, text_size = ingame_font.render("PLAY",False,'Black'), (188/800 * SCREEN_WIDTH, 70/450 * SCREEN_HEIGHT)
text_surface = pygame.transform.scale(text_surface, (text_size))
text_rect = text_surface.get_rect()
# Easy, Standard and Unfair AI faces
difficulty_select_size = 1/4 * SCREEN_WIDTH, 1/4 * SCREEN_WIDTH
ingame_enemy_size = 1/3 * SCREEN_WIDTH, 1/3 * SCREEN_WIDTH
easy_surface, standard_surface, unfair_surface = pygame.image.load('assets/sprites/easy/state1.png'), pygame.image.load('assets/sprites/standard/state1.png'), pygame.image.load('assets/sprites/unfair/state1.png')
easy_surface, standard_surface, unfair_surface = pygame.transform.scale(easy_surface, (difficulty_select_size)), pygame.transform.scale(standard_surface, (difficulty_select_size)), pygame.transform.scale(unfair_surface, (difficulty_select_size))
easy_rect, standard_rect, unfair_rect = easy_surface.get_rect(), standard_surface.get_rect(), unfair_surface.get_rect()
# Rock, Paper, Scissor, Revolver Buttons and HP heart
button_size, heart_size = (1/8 * SCREEN_WIDTH, 1/8 * SCREEN_WIDTH), (1/6 * SCREEN_WIDTH, 1/6 * SCREEN_WIDTH)
rock_surface, paper_surface, scissor_surface = pygame.image.load('assets/sprites/ingame/rock.png'), pygame.image.load('assets/sprites/ingame/paper.png'), pygame.image.load('assets/sprites/ingame/scissor.png')
rock_surface, paper_surface, scissor_surface = pygame.transform.scale(rock_surface, (button_size)), pygame.transform.scale(paper_surface, (button_size)), pygame.transform.scale(scissor_surface, (button_size))
heart_surface = pygame.image.load('assets/sprites/ingame/heart.png')
heart_surface = pygame.transform.scale(heart_surface, (heart_size))
hp_size = 1/10 * SCREEN_WIDTH, 1/10 * SCREEN_HEIGHT
rock_rect, paper_rect, scissor_rect = rock_surface.get_rect(), paper_surface.get_rect(), scissor_surface.get_rect()
heart_rect = heart_surface.get_rect()
# Set rectangle centers for game logo, button and text
game_title_rect.center = (CENTRE_WIDTH, 0.75*CENTRE_HEIGHT)
button_rect.center = (CENTRE_WIDTH, 1.25*CENTRE_HEIGHT)
text_rect.center = button_rect.center
easy_rect.center = (0.25*CENTRE_WIDTH,CENTRE_HEIGHT)
standard_rect.center = (CENTRE_WIDTH,CENTRE_HEIGHT)
unfair_rect.center = (1.75*CENTRE_WIDTH,CENTRE_HEIGHT)
rock_rect.center = (0.5*CENTRE_WIDTH,1.5*CENTRE_HEIGHT)
paper_rect.center = (CENTRE_WIDTH, 1.5*CENTRE_HEIGHT)
scissor_rect.center = (1.5*CENTRE_WIDTH, 1.5*CENTRE_HEIGHT)

game_state = "title"

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit() # Quit game if pygame QUIT event met. Opposite of pygame.init()
            exit()
    # Game sprites and whatever drawn here
    game_window.blit(white_bg,(0,0)) # Place surface at position
    if game_state == "title": # Render the game title and play button until user clicks a button
        game_window.blit(game_title_surface,game_title_rect)
        game_window.blit(button_surface,button_rect)
        game_window.blit(text_surface,text_rect)
        for event in events: # Check if play button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_state = "difficulty" # Move on from title screen
                    events.clear()
    if game_state == "difficulty": # Difficulty select screen
        game_window.blit(easy_surface,easy_rect)
        game_window.blit(standard_surface,standard_rect) # Render every difficulty face
        game_window.blit(unfair_surface,unfair_rect)
        for event in events: # Check if difficulty button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos) or standard_rect.collidepoint(event.pos) or unfair_rect.collidepoint(event.pos):
                    is_difficulty_selected = True # Mark difficulty as selected to move on from difficulty select
                    if easy_rect.collidepoint(event.pos):
                        difficulty = 'easy'
                        enemy_sprite = pygame.transform.scale(easy_surface, ingame_enemy_size)
                    elif standard_rect.collidepoint(event.pos): # Assign appropriate difficulty values
                        difficulty = 'standard'
                        enemy_sprite = pygame.transform.scale(standard_surface, ingame_enemy_size)
                    elif unfair_rect.collidepoint(event.pos):
                        difficulty = 'unfair'
                        enemy_sprite = pygame.transform.scale(unfair_surface, ingame_enemy_size)
                    enemy_rect = enemy_sprite.get_rect()
                    enemy_rect.center = CENTRE_WIDTH, 0.5*CENTRE_HEIGHT
                    game_state = "ingame"
    if game_state == "ingame":
        game_window.blit(enemy_sprite, enemy_rect) # Render rock, paper, scissor buttons.
        game_window.blit(rock_surface, rock_rect)
        game_window.blit(paper_surface, paper_rect)
        game_window.blit(scissor_surface, scissor_rect)

    pygame.display.update() # Update display
    clock.tick(60) # 60FPS cap.
    