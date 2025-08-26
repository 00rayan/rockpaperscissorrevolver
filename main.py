import pygame
import random
from sys import exit
import ai_logic

class Player:
    def __init__(self, hp, confidence, last_choice):
        self.hp = hp
        self.confidence = confidence
        self.last_choice = last_choice

class Gameplay:
    def __init__(self, difficulty, chamber_count, turn_number, is_over, winner):
        self.difficulty = difficulty
        self.chamber_count = chamber_count
        self.turn_number = turn_number
        self.is_over = is_over
        self.winner = winner

round_loser = None
loser_name = None
round_feedback_timer = 60

pygame.init() # Initialize pygame

screen_res = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_res.current_h*(3/4), screen_res.current_h*(9/16)
CENTRE_WIDTH = SCREEN_WIDTH // 2
CENTRE_HEIGHT = SCREEN_HEIGHT // 2

game_window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game_title = pygame.display.set_caption("Rock, Paper, Scissor, Revolver")
# Note: once icon made/decided on, add it here. Maybe the idle sprites for the AI
clock = pygame.time.Clock() # Used to cap framerate
ingame_font = pygame.font.Font('assets/fonts/Retro Gaming.ttf',40) # Set font for game

white_bg = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
white_bg.fill("White")

# Get all game assets, and transform and rect appropriately.
# Game title
game_title_surface, game_title_size = pygame.image.load('assets/sprites/other/rpsrevolverlogo.png'), (768/1024 * SCREEN_WIDTH,192/768 * SCREEN_HEIGHT) # Get logo image (256x64)
game_title_surface = pygame.transform.scale(game_title_surface, (game_title_size)) # Set size RELATIVE to screen, so it's same regardless of resolution.
game_title_rect = game_title_surface.get_rect()
# Button and text
button_surface, button_size = pygame.image.load('assets/sprites/buttons/buttonflat.png'), (250/800 * SCREEN_WIDTH, 70/450 * SCREEN_HEIGHT)
button_surface = pygame.transform.scale(button_surface, (button_size)) # Set size relative again.
button_rect = button_surface.get_rect()
text_surface, text_size = ingame_font.render("PLAY",False,'Black'), (195/800 * SCREEN_WIDTH, 70/450 * SCREEN_HEIGHT)
text_surface = pygame.transform.scale(text_surface, (text_size))
text_rect = text_surface.get_rect()
# Easy, Standard and Unfair AI faces
difficulty_select_size = 1/4 * SCREEN_WIDTH, 1/4 * SCREEN_WIDTH
ingame_enemy_size = 1/3 * SCREEN_WIDTH, 1/3 * SCREEN_WIDTH
easy_surface, standard_surface, unfair_surface = pygame.image.load('assets/sprites/easy/state1.png'), pygame.image.load('assets/sprites/standard/state1.png'), pygame.image.load('assets/sprites/unfair/state1.png')
easy_surface, standard_surface, unfair_surface = pygame.transform.scale(easy_surface, (difficulty_select_size)), pygame.transform.scale(standard_surface, (difficulty_select_size)), pygame.transform.scale(unfair_surface, (difficulty_select_size))
easy_rect, standard_rect, unfair_rect = easy_surface.get_rect(), standard_surface.get_rect(), unfair_surface.get_rect()
# Rock, Paper, Scissor, Revolver Buttons and HP heart
choice_button_size, heart_size = (1/5 * SCREEN_WIDTH, 1/5 * SCREEN_WIDTH), (1/15 * SCREEN_WIDTH, 1/15 * SCREEN_WIDTH)
rock_surface, paper_surface, scissor_surface = pygame.image.load('assets/sprites/ingame/rock.png'), pygame.image.load('assets/sprites/ingame/paper.png'), pygame.image.load('assets/sprites/ingame/scissor.png')
rock_surface, paper_surface, scissor_surface = pygame.transform.scale(rock_surface, (choice_button_size)), pygame.transform.scale(paper_surface, (choice_button_size)), pygame.transform.scale(scissor_surface, (choice_button_size))
player_heart_surface = pygame.image.load('assets/sprites/ingame/heart.png')
player_heart_surface = pygame.transform.scale(player_heart_surface, (heart_size))
ai_heart_surface = pygame.image.load('assets/sprites/ingame/heart.png')
ai_heart_surface = pygame.transform.scale(player_heart_surface, (heart_size))

hp_size = 1/10 * SCREEN_WIDTH, 1/10 * SCREEN_HEIGHT
rock_rect, paper_rect, scissor_rect = rock_surface.get_rect(), paper_surface.get_rect(), scissor_surface.get_rect()
player_heart_rect = player_heart_surface.get_rect()
ai_heart_rect = ai_heart_surface.get_rect()
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

ai_heart_rect.topleft = (0,0)
player_heart_rect.bottomleft = (0, SCREEN_HEIGHT)

game_state = "title"

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit() # Quit game if pygame QUIT event met. Opposite of pygame.init()
            exit()
    # Game sprites and whatever drawn here
    game_window.blit(white_bg,(0,0)) # Place surface at position

# Title screen game state
    if game_state == "title": 
        game_window.blit(game_title_surface,game_title_rect) # Render the game title and play button until user clicks a button
        game_window.blit(button_surface,button_rect)
        game_window.blit(text_surface,text_rect)
        for event in events: # Check if play button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_state = "difficulty" # Move on from title screen
                    events.clear()

# Difficulty select game state
    if game_state == "difficulty": 
        game_window.blit(easy_surface,easy_rect)
        game_window.blit(standard_surface,standard_rect) # Render every difficulty face
        game_window.blit(unfair_surface,unfair_rect)
        for event in events: # Check if difficulty button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos) or standard_rect.collidepoint(event.pos) or unfair_rect.collidepoint(event.pos):
                    game_state = "ingame" # Mark difficulty as selected to move on from difficulty select
                    if easy_rect.collidepoint(event.pos):
                        gameplay_object = Gameplay('easy',1,1,False,None)
                        ai_object, player_object = Player(1,2,None), Player(3,1,None)
                        enemy_sprite = pygame.transform.scale(easy_surface, ingame_enemy_size)
                    elif standard_rect.collidepoint(event.pos): # Assign appropriate difficulty values
                        gameplay_object = Gameplay('standard',6,1,False,None)
                        ai_object, player_object = Player(2,1,None), Player(2,1,None)
                        enemy_sprite = pygame.transform.scale(standard_surface, ingame_enemy_size)
                    elif unfair_rect.collidepoint(event.pos):
                        gameplay_object = Gameplay('unfair',6,1,False,None)
                        ai_object, player_object = Player(2,1,None), Player(1,1,None)
                        enemy_sprite = pygame.transform.scale(unfair_surface, ingame_enemy_size)
                    enemy_rect = enemy_sprite.get_rect()
                    enemy_rect.center = CENTRE_WIDTH, 0.5*CENTRE_HEIGHT
                   
# Gameplay game state
    if game_state == "ingame" and not gameplay_object.is_over:
        ai_hp_surface = ingame_font.render(f'{ai_object.hp}', False, 'Black') # Create surface for AI and player HP
        player_hp_surface = ingame_font.render(f'{player_object.hp}', False, 'Black')
        ai_hp_rect, player_hp_rect, = ai_hp_surface.get_rect(), player_hp_surface.get_rect() # Create rect for AI and player HP for easy placement
        ai_hp_rect.topleft, player_hp_rect.bottomleft = (0.075*SCREEN_WIDTH,0), (0.075*SCREEN_WIDTH,SCREEN_HEIGHT)

        game_window.blit(enemy_sprite, enemy_rect) # Render rock, paper, scissor buttons.
        game_window.blit(rock_surface, rock_rect)
        game_window.blit(paper_surface, paper_rect)
        game_window.blit(scissor_surface, scissor_rect)
        game_window.blit(ai_heart_surface, ai_heart_rect)
        game_window.blit(ai_hp_surface, ai_hp_rect)
        game_window.blit(player_heart_surface, player_heart_rect)
        game_window.blit(player_hp_surface, player_hp_rect)
        for event in events:
            player_move = None
            if event.type == pygame.MOUSEBUTTONDOWN: # Detect if player has chosen.
                if rock_rect.collidepoint(event.pos):
                    player_move = 1
                elif paper_rect.collidepoint(event.pos):
                    player_move = 2
                elif scissor_rect.collidepoint(event.pos):
                    player_move = 3
            if player_move != None:
                round_feedback_timer = 90
                ai_move = ai_logic.weight_and_predict_move('player_data',player_object.last_choice,ai_object.confidence) # Get AI move.
                player_object.last_choice = player_move
                chamber = gameplay_object.chamber_count
                if player_move == 1 and ai_move == 2 or player_move == 2 and ai_move == 3 or player_move == 3 and ai_move == 1: # Reward winner score
                    round_loser = player_object # Assign player as loser
                    loser_name = 'Player'
                    if gameplay_object.difficulty != 'easy' and ai_object.confidence < 2:
                        ai_object.confidence += 0.1                        
                elif player_move == ai_move:
                    round_loser = None
                    loser_name = 'No one'
                    if gameplay_object.difficulty != 'easy' and gameplay_object.chamber_count != 1:
                        gameplay_object.chamber_count -= 1 # Progress chamber if tie, and chamber size not 1
                elif player_move == 1 and ai_move == 3 or player_move == 2 and ai_move == 1 or player_move == 3 and ai_move == 2:
                    round_loser = ai_object # Assign AI as loser
                    loser_name = 'AI'
                    if gameplay_object.difficulty != 'easy' and ai_object.confidence > 0.5:
                        ai_object.confidence -= 0.1   
                roulette_spin = random.randint(1,chamber) # Spin number 1-chambersize
                if roulette_spin == 1 and round_loser != None: # Fire revolver if 1 is spun
                    round_loser.hp -= 1
        if loser_name != None:
            loser_status_surface = ingame_font.render(f'{loser_name} lost!',False,'Red')
            loser_status_rect = loser_status_surface.get_rect()
            loser_status_rect.center = (CENTRE_WIDTH, CENTRE_HEIGHT)
            if round_feedback_timer > 0:
                game_window.blit(loser_status_surface, loser_status_rect)
                round_feedback_timer -= 1
            
                    
        if ai_object.hp == 0 or player_object.hp == 0:
            if ai_object.hp == 0:
                gameplay_object.winner = 'Player'
            else:
                gameplay_object.winner = 'AI'
            gameplay_object.is_over = True
            game_state = "results"
            round_feedback_timer = 0

    if game_state == "results":
        winner_text = ingame_font.render(f'{gameplay_object.winner} wins!', False, 'Green')
        winner_rect = winner_text.get_rect()

        menu_button_rect = button_surface.get_rect()
        menu_text = ingame_font.render("MENU", False, 'Black')
        menu_text = pygame.transform.scale(menu_text, (text_size))
        menu_text_rect = menu_text.get_rect() 
        menu_button_rect.center = (CENTRE_WIDTH, 1.1*CENTRE_HEIGHT)
        menu_text_rect.center = menu_button_rect.center
        winner_rect.center = (CENTRE_WIDTH, 0.8*CENTRE_HEIGHT)
        game_window.blit(winner_text, winner_rect)
        game_window.blit(button_surface, menu_button_rect)
        game_window.blit(menu_text, menu_text_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if menu_button_rect.collidepoint(event.pos):
                    game_state = "title"
                    

    pygame.display.update() # Update display
    clock.tick(60) # 60FPS cap.
    