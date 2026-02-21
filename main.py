import pygame
import random
import os
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

class button_sprite(pygame.sprite.Sprite): # Sprite class for all button sprites
    def __init__(self,asset,size,position):
        super().__init__()
        self.image, self.size = pygame.image.load(asset), (size)
        self.image = pygame.transform.scale(self.image, (self.size))
        self.rect = self.image.get_rect()
        self.rect.center = position
    
class enemy_sprite(pygame.sprite.Sprite):
    def __init__(self,asset,size,position):
        super().__init__()
        self.image, self.size = pygame.image.load(asset), (size)
        self.image = pygame.transform.scale(self.image, (self.size))
        self.rect = self.image.get_rect()
        self.rect.center = position

round_loser = None
loser_name = None

pygame.init() # Initialize pygame
 
screen_res = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CENTRE_WIDTH = SCREEN_WIDTH // 2
CENTRE_HEIGHT = SCREEN_HEIGHT // 2

game_window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game_title = pygame.display.set_caption("Rock, Paper, Scissor, Revolver")
# Note: once icon made/decided on, add it here. Maybe the idle sprites for the AI
clock = pygame.time.Clock() # Used to cap framerate
ingame_font = pygame.font.Font('assets/fonts/Retro Gaming.ttf',40) # Set font for game

rps_background = pygame.image.load('assets/sprites/other/rpspattern.png') # Define background colors (foundation to be replaced with actual assets/anims)
bg_horizontal_size, bg_vertical_size = rps_background.get_size()
rps_x, rps_y = 0, 0
bg_width, bg_height = rps_background.get_size()
difficulty_background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
difficulty_background.fill("grey")
ingame_background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))


# Get all game assets, and transform and rect appropriately. Turn into sprites
# Game title
game_title_surface, game_title_size = pygame.image.load('assets/sprites/other/rpsrevolverlogo.png'), (768/1024 * SCREEN_WIDTH,192/768 * SCREEN_HEIGHT) # Get logo image (256x64)
game_title_surface = pygame.transform.scale(game_title_surface, (game_title_size)) # Set size RELATIVE to screen, so it's same regardless of resolution.
game_title_rect = game_title_surface.get_rect()
# Button and text

button_surface, button_size, button_center = 'assets/sprites/buttons/playbuttonflat.png', (250/800 * SCREEN_WIDTH, 70/450 * SCREEN_HEIGHT), (CENTRE_WIDTH, 1.25*CENTRE_HEIGHT)
play_button = button_sprite(button_surface,button_size,button_center)
sprites_group = pygame.sprite.Group()
text_surface, text_size = ingame_font.render("PLAY",False,'Black'), (195/800 * SCREEN_WIDTH, 70/450 * SCREEN_HEIGHT)
text_surface = pygame.transform.scale(text_surface, (text_size))
text_rect = text_surface.get_rect()
# Easy, Standard and Unfair AI faces and sizes
easy_center = (0.25*CENTRE_WIDTH,CENTRE_HEIGHT)
standard_center = (CENTRE_WIDTH,CENTRE_HEIGHT)
unfair_center = (1.75*CENTRE_WIDTH,CENTRE_HEIGHT)
difficulty_select_size = 1/4 * SCREEN_WIDTH, 1/4 * SCREEN_WIDTH
ingame_enemy_size = 1/3 * SCREEN_WIDTH, 1/3 * SCREEN_WIDTH
easy_asset, standard_asset, unfair_asset = 'assets/sprites/easy/state1.png', 'assets/sprites/standard/state1.png', 'assets/sprites/unfair/state1.png'
easy_difficulty = enemy_sprite(easy_asset,difficulty_select_size,easy_center)
standard_difficulty = enemy_sprite(standard_asset,difficulty_select_size,standard_center)
unfair_difficulty = enemy_sprite(unfair_asset,difficulty_select_size,unfair_center)
# Rock, Paper, Scissor, Revolver Buttons and HP heart
choice_button_size, heart_size = (1/5 * SCREEN_WIDTH, 1/5 * SCREEN_WIDTH), (1/15 * SCREEN_WIDTH, 1/15 * SCREEN_WIDTH)
rock_surface, paper_surface, scissor_surface = pygame.image.load('assets/sprites/ingame/rock.png'), pygame.image.load('assets/sprites/ingame/paper.png'), pygame.image.load('assets/sprites/ingame/scissor.png')
rock_surface, paper_surface, scissor_surface = pygame.transform.scale(rock_surface, (choice_button_size)), pygame.transform.scale(paper_surface, (choice_button_size)), pygame.transform.scale(scissor_surface, (choice_button_size))
player_heart_surface = pygame.image.load('assets/sprites/ingame/heart.png')
player_heart_surface = pygame.transform.scale(player_heart_surface, (heart_size))   
ai_heart_surface = pygame.image.load('assets/sprites/ingame/heart.png')
ai_heart_surface = pygame.transform.scale(player_heart_surface, (heart_size))

enemy_size = CENTRE_WIDTH, 0.5*CENTRE_HEIGHT
hp_size = 1/10 * SCREEN_WIDTH, 1/10 * SCREEN_HEIGHT
rock_rect, paper_rect, scissor_rect = rock_surface.get_rect(), paper_surface.get_rect(), scissor_surface.get_rect()
player_heart_rect = player_heart_surface.get_rect()
ai_heart_rect = ai_heart_surface.get_rect()
# Set rectangle centers for game logo, button and text
game_title_rect.center = (CENTRE_WIDTH, 0.75*CENTRE_HEIGHT)
rock_rect.center = (0.5*CENTRE_WIDTH,1.5*CENTRE_HEIGHT)
paper_rect.center = (CENTRE_WIDTH, 1.5*CENTRE_HEIGHT)
scissor_rect.center = (1.5*CENTRE_WIDTH, 1.5*CENTRE_HEIGHT)

ai_heart_rect.topright = (SCREEN_WIDTH,0)
player_heart_rect.bottomleft = (0, SCREEN_HEIGHT)

game_state = "title"
player_stat = None

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit() # Quit game if pygame QUIT event met. Opposite of pygame.init()
            exit()
    # Game sprites and whatever drawn here
# Title screen game state
    if game_state == "title":
        sprites_group.add(play_button) 
        game_window.blit(rps_background,(rps_x,rps_y)) # Draw white background in main menu (to be replaced)
        if rps_x > (SCREEN_WIDTH-bg_horizontal_size) and rps_y > (SCREEN_HEIGHT-bg_vertical_size):
            rps_x -= 1
            rps_y -= 1
        else:
            rps_x = 0
            rps_y = 0
        game_window.blit(game_title_surface,game_title_rect) # Render the game title and play button until user clicks a button
        sprites_group.draw(game_window)
        for event in events: # Check if play button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(play_button,sprites_group,True):
                    sprites_group.remove(play_button)
                    game_state = "difficulty" # Move on from title screen
                    sprites_group.add(easy_difficulty)
                    sprites_group.add(standard_difficulty)
                    sprites_group.add(unfair_difficulty)
                    events.clear()

# Difficulty select game state
    if game_state == "difficulty": 
        game_window.blit(difficulty_background,(0,0)) # Draw gray background in difficulty select (to be replaced)

        sprites_group.draw(game_window)  # Render every difficulty face
        for event in events: # Check if difficulty button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_difficulty.rect.collidepoint(event.pos) or standard_difficulty.rect.collidepoint(event.pos) or unfair_difficulty.rect.collidepoint(event.pos):
                    sprites_group.remove(easy_difficulty)
                    sprites_group.remove(standard_difficulty)
                    sprites_group.remove(unfair_difficulty)
                    hp_color = 'Black'
                    game_state = "ingame" # Mark difficulty as selected to move on from difficulty select
                    is_first = 'F'
                    is_first_bool = True
                    if easy_difficulty.rect.collidepoint(event.pos):
                        ingame_background.fill("white")
                        gameplay_object = Gameplay('easy',1,1,False,None)
                        ai_object, player_object = Player(1,2,None), Player(3,1,None)
                        enemy_sprite_object = enemy_sprite('assets/sprites/easy/state1.png',ingame_enemy_size,enemy_size)
                    elif standard_difficulty.rect.collidepoint(event.pos): # Assign appropriate difficulty values
                        ingame_background.fill("gray90")
                        gameplay_object = Gameplay('standard',6,1,False,None)
                        ai_object, player_object = Player(2,1,None), Player(2,1,None)
                        enemy_sprite_object = enemy_sprite('assets/sprites/standard/state1.png',ingame_enemy_size,enemy_size)
                    elif unfair_difficulty.rect.collidepoint(event.pos):
                        hp_color = 'White'
                        ingame_background.fill("gray12")
                        gameplay_object = Gameplay('unfair',6,1,False,None)
                        ai_object, player_object = Player(2,1,None), Player(1,1,None)
                        enemy_sprite_object = enemy_sprite('assets/sprites/unfair/state1.png',ingame_enemy_size,enemy_size)
# Gameplay game state
    if game_state == "ingame" and not gameplay_object.is_over:
        game_window.blit(ingame_background,(0,0)) # Draw blue background ingame (to be replaced)
        if not os.path.exists(f"player_data.txt"):
            with open(f"player_data.txt","w") as file: # Check for existing save file, create if not found.
                file.close()
        player_data_for_write = open(f"player_data.txt", "a") # Open file in append mode, as to not overwrite data.
        all_player_moves = ai_logic.get_player_data()
        ai_hp_surface = ingame_font.render(f'{ai_object.hp}', False, hp_color) # Create surface for AI and player HP
        player_hp_surface = ingame_font.render(f'{player_object.hp}', False, hp_color)
        ai_hp_rect, player_hp_rect, = ai_hp_surface.get_rect(), player_hp_surface.get_rect() # Create rect for AI and player HP for easy placement
        ai_hp_rect.topright, player_hp_rect.bottomleft = (0.925*SCREEN_WIDTH,0), (0.075*SCREEN_WIDTH,SCREEN_HEIGHT)
        # Render rock, paper, scissor buttons.
        game_window.blit(rock_surface, rock_rect)
        game_window.blit(paper_surface, paper_rect)
        game_window.blit(scissor_surface, scissor_rect)
        game_window.blit(ai_heart_surface, ai_heart_rect)
        game_window.blit(ai_hp_surface, ai_hp_rect)
        game_window.blit(player_heart_surface, player_heart_rect)
        game_window.blit(player_hp_surface, player_hp_rect)
        sprites_group.add(enemy_sprite_object)
        sprites_group.draw(game_window)
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
                round_feedback_timer = 45
                ai_move = ai_logic.weight_and_predict_move(all_player_moves,player_object.last_choice,ai_object.confidence, is_first_bool, player_stat) # Get AI move.
                player_object.last_choice = player_move
                if player_move == 1 and ai_move == 2 or player_move == 2 and ai_move == 3 or player_move == 3 and ai_move == 1: # Reward winner score
                    round_loser = player_object # Assign player as loser
                    loser_name = 'Player'
                    player_stat = 'L' # Player data to store (win/lose/tie)
                    if gameplay_object.difficulty != 'easy' and ai_object.confidence < 2:
                        ai_object.confidence += 0.1                        
                elif player_move == ai_move:
                    round_loser = None
                    loser_name = 'No one'
                    player_stat = 'T' # Player data to store (win/lose/tie)
                    if gameplay_object.difficulty != 'easy' and gameplay_object.chamber_count != 1:
                        gameplay_object.chamber_count -= 1 # Progress chamber if tie, and chamber size not 1
                elif player_move == 1 and ai_move == 3 or player_move == 2 and ai_move == 1 or player_move == 3 and ai_move == 2:
                    round_loser = ai_object # Assign AI as loser
                    loser_name = 'AI'
                    player_stat = 'W' # Player data to store (win/lose/tie)
                    if gameplay_object.difficulty != 'easy' and ai_object.confidence > 0.5:
                        ai_object.confidence -= 0.1
                chamber = gameplay_object.chamber_count  
                new_data = f"{str(player_move)}{player_stat}{is_first}\n"
                is_first = "_"
                is_first_bool = False
                player_data_for_write.write(new_data) # Update player text file to include last input if valid
                roulette_spin = random.randint(1,chamber) # Spin number 1-chambersize
                if roulette_spin == 1 and round_loser != None: # Fire revolver if 1 is spun
                    gameplay_object.chamber_count = 6
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
            events.clear()
            game_state = "results"
            round_feedback_timer = 0
        

    if game_state == "results":
        sprites_group.remove(enemy_sprite_object)
        menu_button_surface, button_size, button_center = 'assets/sprites/buttons/menubuttonflat.png', (250/800 * SCREEN_WIDTH, 70/450 * SCREEN_HEIGHT), (CENTRE_WIDTH, 1.1*CENTRE_HEIGHT)
        game_window.fill("White") # Draw white background in results (to be replaced)
        menu_button = button_sprite(menu_button_surface,button_size,button_center)
        sprites_group.add(menu_button)
        sprites_group.draw(game_window)
        player_data_for_write.close()
        winner_text = ingame_font.render(f'{gameplay_object.winner} wins!', False, 'Green')
        winner_rect = winner_text.get_rect()
        winner_rect.center = (CENTRE_WIDTH, 0.8*CENTRE_HEIGHT)
        game_window.blit(winner_text, winner_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if pygame.sprite.spritecollide(menu_button,sprites_group,True):
                    sprites_group.remove(menu_button)
                    game_state = "title"
                    events.clear()

    pygame.display.flip() # Update display
    clock.tick(60) # 60FPS cap.
