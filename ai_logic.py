# Import libraries
import random
import os

# No GUI as of now, but might add a GUI with pygame or tkinter, preferably pygame. This is the one of last steps once the AI is actually a challenge and 90% complete. 
# Note: change the win condition, not first to 10, russian roulette, with varying health per difficulty.

def get_player_data(): # Turns the playerdata into an easily readable array for the program.
    player_data = open(f"player_data.txt", "r") # Open file in read mode, to look at patterns.
    all_player_moves = [line.strip() for line in player_data.readlines()] # Strip of "\n" so the text file is clean
    player_data.close() # Close file to free up memory
    return all_player_moves

def update_highest_chains(favorite1,favorite2,favorite3,last_button,current_chain,time_group): # Part of the get_favorite_and_highest_chains() module.
    if last_button == "1":
        if current_chain > favorite1[time_group]:
            favorite1[time_group] = current_chain
    if last_button == "2":
        if current_chain > favorite2[time_group]:
            favorite2[time_group] = current_chain
    if last_button == "3":
        if current_chain > favorite3[time_group]:
            favorite3[time_group] = current_chain
    return

def get_favorite_and_highest_chains(player_moves_list): # Calculates 2 values, favorite and highest chains. really long, break this down more? Might axe later
    # Count total times each button pressed
    one_counter = [0,0]
    two_counter = [0,0]
    three_counter = [0,0]

    # Count highest chain press of each button
    highest_one_chains = [1,1] # Pos 1: overall, Pos 2: recent   
    highest_two_chains = [1,1]
    highest_three_chains = [1,1]
    most_chained_buttons = [0,0]
    highest_chains = [0,0]
    favorite_button = [0,0]
    
    # Declare variables used in the loop
    current_chain = 1
    last = None
    start = 0
    group = 0
    position = 0
    done = False
    end = len(player_moves_list)

    while not done:
        for index in range(0, end): # Count for entire player moves list
            position = start + index
            if player_moves_list[position] == "1":
                one_counter[group] += 1
            elif player_moves_list[position] == "2": # Increase the respective counters for each button
                two_counter[group] += 1
            elif player_moves_list[position] == "3":
                three_counter[group] += 1
            if last == player_moves_list[position]:
                current_chain += 1
            else:
                update_highest_chains(highest_one_chains,highest_two_chains,highest_three_chains,last,current_chain,group)
                current_chain = 1
            last = player_moves_list[position]
            # Final run to get the most chained button.
            update_highest_chains(highest_one_chains,highest_two_chains,highest_three_chains,last,current_chain,group)
        # Assign most frequent button
        if one_counter > two_counter and one_counter > three_counter:
            favorite_button[group] = 1
        elif two_counter > one_counter and two_counter > three_counter:
            favorite_button[group] = 2
        elif three_counter > one_counter and three_counter > two_counter:
            favorite_button[group] = 3
        else:
            favorite_button[group] = random.randint(1,3) # TEMPORARY!!! Fallback for tied favorite buttons, replace this and line 93 with a better solution
        if group == 1 or len(player_moves_list) < 20:
            done = True
        start = len(player_moves_list) - 20 # Start at last 20 inputs
        group = 1 # Set group to 1 so inputs stored in the position for recent inputs
        end = 20 # Declare end to 20, for last 20 inputs

    # Identify which button is pressed the most times in a row
    for time in range (0,1):    
        if highest_one_chains[time] > highest_two_chains[time] and highest_one_chains[time] > highest_three_chains[time]:
            most_chained_buttons[time] = 1
            highest_chains[time] = highest_one_chains[time]
        elif highest_two_chains[time] > highest_one_chains[time] and highest_two_chains[time] > highest_three_chains[time]:
            most_chained_buttons[time] = 2
            highest_chains[time] = highest_two_chains[time]
        elif highest_three_chains[time] > highest_one_chains[time] and highest_three_chains[time] > highest_two_chains[time]:
            most_chained_buttons[time] = 3
            highest_chains[time] = highest_three_chains[time]
        else:
            most_chained_buttons[time] = random.randint(1,3) # TEMPORARY!!! Fallback if any chains are tied, replace later with something better
    
    return most_chained_buttons, favorite_button, highest_chains

def find_and_store_patterns(player_moves_list, patterns_list): # Unfinished, Finds and STORES repeating patterns in the player data, for hardmode, coding this is even harder. 
    patterns = [[]] # Stores recurring patterns at patterns[x][0] and how many times they've repeated in patterns[x][1], corresponding to the same.
    end = len(player_moves_list)

    return patterns
    
def complex_pattern_process(num, player_moves_list, current_patterns, counter_requirement): # I'm lost as hell
    return

def check_for_patterns(last_2_moves, patterns_list): # Used only to check for pre-existing patterns. Does NOT check playerdata, used along find_and_store_patterns(). Please send help
    first_move, second_move = last_2_moves[0], last_2_moves[1]
    print(last_2_moves) # DEBUG CODE, remove after code is confirmed to work.
    for index in range(0, len(patterns_list)):
        for pos in range (0,len(patterns_list[pos])):
            if patterns_list[index][pos] == first_move and patterns_list[index][pos+1] == second_move:
                next_move = patterns_list[index][pos+2]
                break
    return next_move

def simple_patterns(last_move, player_moves_list):
    one_counter, two_counter, three_counter = 0,0,0
    next_move = None
    for index in range(0,len(player_moves_list)):
        if player_moves_list[index] == last_move:
            if player_moves_list[index+1] == '1':
                one_counter += 1
            elif player_moves_list[index+1] == '2':
                two_counter += 1
            else:
                three_counter +=1
    if one_counter > two_counter and one_counter > three_counter:
        next_move = 1
    elif two_counter > one_counter and two_counter > three_counter:
        next_move = 2
    elif three_counter > one_counter and three_counter > two_counter:
        next_move = 3
    else:
        next_move = None # Can't predict. (ok it can between the 2 highest but im too lazy)
    return next_move

def weight_and_predict_move(player_moves_list, last_choice, confidence): # Calls functions to get the data values, then weights, calculates and returns the move.
    if len(player_moves_list) < 5:
        move = random.randint(1,3) # TEMPORARY!!! Fallback if data insufficient, pure RNG. might update this later to use an "average person" playerdata. 
        return move
        
    # Count highest chain of each button pressed in a row.
    most_chained_buttons, favorite_button, highest_chains = get_favorite_and_highest_chains(player_moves_list)

    # Guess logic, give each button RNG weight, 5% chance of mindless RNG. (Tweak this as you go)
    weights = [0,0,0] # button 1, 2, 3, remainder = TOTAL RNG

    # Declare all weights, for predictability of player and favorite weights.    
    multiplier = 1
    very_consistent_last_choice_weight, inconsistent_last_choice_weight, consistent_last_choice_weight  = 10/3, -5, 5/3 
    favorite_weight_overall, favorite_weight_recent = 10/3, 5
    chain_weight_overall, chain_weight_recent  = 5/3, 5

    # 1. Decide if player is likely to chain or not, how consistent.
    if last_choice != None:
        for period in range (0,2):
            if period == 1:
                multiplier = 2
            if highest_chains[period] >= 4: # VERY CONSISTENT, +10 weight to last choice.
                weights[last_choice-1] += very_consistent_last_choice_weight*multiplier*confidence
            if highest_chains[period] <= 2: # VERY INCONSISTENT, -5 weight to last choice. 
                weights[last_choice-1] += inconsistent_last_choice_weight*multiplier*confidence
            else: # Somewhat consistent, +5 weight to last choice. 
                weights[last_choice-1] += consistent_last_choice_weight*multiplier*confidence

    # Overall biggest chain and favorite
    overall_chained, overall_favorite = most_chained_buttons[0], favorite_button[0] 
    weights[overall_chained - 1] += chain_weight_overall*confidence # Weight for most chained button 
    weights[overall_favorite - 1] += favorite_weight_overall*confidence # Weight for favorite button.

    # Recent biggest chain and favorite
    recent_chained, recent_favorite = most_chained_buttons[1], favorite_button[1]
    weights[recent_chained - 1] += chain_weight_recent*confidence # Weight for most chained button.
    weights[recent_favorite - 1] += favorite_weight_recent*confidence # Weight for favorite button.
    
    # Do simple pattern checks, add weight to corresponding button.
    patterns_button_weight = 8 # Heaviest weight by far.
    patterns_button = simple_patterns(last_choice, player_moves_list)
    if patterns_button != None:
        weights[patterns_button - 1] += patterns_button_weight

    # Use assigned RNG weight
    random_number = random.randint(0,100)
    if random_number < weights[0]: 
        move = 1 # In range of button 1 weight
    elif random_number > weights[0] and random_number < weights[0] + weights[1]:
        move = 2 # In range of button 2 weight
    elif random_number > weights[0] + weights[1] and random_number < sum(weights):
        move = 3 # In range of button 3 weight 
    else:
        move = random.randint(1,3) # In range of wildcard weight
    
    return move

# def main(): # Main gameplay loop, soon to be removed, as pygame is now functional.
#     if not os.path.exists(f"player_data.txt"):
#         with open(f"player_data.txt","w") as file: # Check for existing save file, create if not found.
#             file.close()
#     difficulty = int(input("Choose difficulty: (1: Practice/2: Basic/3: Unfair)"))
#     if difficulty == 1:
#         roulette_count = 1 # Practice difficulty has no roulette, you don't deserve it.
#     elif difficulty == 2:
#         roulette_count = 3 # 1 in 3 chance for basic.
#     else:
#         roulette_count = 6 # 6 chamber roulette BUT chance increases.
#     # Start both scores as 0
#     turns = 0 # Used to trigger repeating pattern check later   
#     confidence_multipler = 1 # Multiplier added on the weightings that changes by 0.1 every win/lose
#     ai_health = 3 
#     player_health = 3
#     ai_roulette_death_number = random.randint(1,roulette_count) # Assign random number from 1 to 6 which kills AI/player in russian roulette
#     player_roulette_death_number = random.randint(1,roulette_count)
#     last_choice = random.randint(1,3) # Placeholder last choice, since player hasn't made one yet.
    
#     # Main gameplay loop, continues until AI/player reach 10 points. Getting axed in favor of OOP very soon.
#     while ai_health != 0 and player_health != 0:
#         player_data_for_write = open(f"player_data.txt", "a") # Open file in append mode, as to not overwrite data. 
#         player_data_for_read = get_player_data()
#         ai_prediction = weight_and_predict_move(player_data_for_read, last_choice,confidence_multipler)
#         if ai_prediction == 1: # Prediction = rock, move = paper
#             ai_move = 2
#         elif ai_prediction == 2: # Prediction = paper, move = scissors
#             ai_move = 3
#         else: # Prediction = scissors, move = rock
#             ai_move = 1

#         print(f"AI Health: {ai_health}    Player Health: {player_health}")
#         player_move = input("Choose which button (1. Rock/2. Paper/3. Scissors): ") # Get player choice
#         if player_move != '1' and player_move != '2' and player_move != '3': # Input validation to prevent save file corruption
#             print("Invalid input. ") # Error handling
#             return
#         player_move = int(player_move)
#         last_choice = player_move # Store current player choice to be used in next turn for AI.
#         new_data = f"{str(player_move)}\n"
#         player_data_for_write.write(new_data) # Update player text file to include last input if valid
        
#         if player_move == 1 and ai_move == 2 or player_move == 2 and ai_move == 3 or player_move == 3 and ai_move == 1: # Reward winner score
#             print("AI beat player hand!")
#             spin_number = random.randint(1,roulette_count)
#             if spin_number == player_roulette_death_number:
#                 print("Unlucky, you got shot!")
#                 player_roulette_death_number = random.randint(1,roulette_count)
#                 player_health -= 1
#             else:
#                 print("Lucky, gun didn't go off!")
#             if confidence_multipler < 1.5:
#                 confidence_multipler += 0.1
#             roulette_count -= 1
#             player_roulette_death_number = random.randint(1,roulette_count)
#             ai_roulette_death_number = random.randint(1,roulette_count)
#         elif player_move == ai_move:
#             print("Tie!")
#         else:
#             print("Player beat AI hand!")
#             spin_number = random.randint(1,roulette_count)
#             if spin_number == ai_roulette_death_number:
#                 print("AI got shot!")
#                 ai_roulette_death_number = random.randint(1,roulette_count)
#                 ai_health -= 1
#             else:
#                 print("AI got lucky!")
#             if confidence_multipler > 0.5:
#                 confidence_multipler -= 0.1
#             roulette_count -= 1
#             if roulette_count == 0:
#                 roulette_count = 6
#             player_roulette_death_number = random.randint(1,roulette_count)
#             ai_roulette_death_number = random.randint(1,roulette_count  )
#         # os.system('cls') # Clear console for neatness.

#     # Print a suitable game over message (Win/Lose)
#     if player_health == 0:
#         print("Game over, I've won.")
#     else:
#         print("Bravo, you win.")
#     player_data_for_write.close() # Close file at the end to free up memory.
#     retry = input("Play again? (Y/N): ")
#     if retry != 'Y':
#         exit()
#     return

# while True:
#    main()

# # TEMPORARY !!! For testing the complex pattern finding, don't remove until verified working.
# player_moves_list = get_player_data('rayan')
# patterns_list = []
# find_and_store_patterns(player_moves_list, patterns_list)