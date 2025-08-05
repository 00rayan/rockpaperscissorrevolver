# Import libraries
import random
import os

# Player chooses between 3 buttons, AI predicts which one user will press based on previous patterns, user wins if AI fails to predict. AI wins if it predicts correctly. First to 10 points wins
# No GUI as of now, but might add a GUI with pygame or tkinter, preferably pygame.

def get_player_data(name): # Turns the playerdata into an easily readable array for the program.
    player_data = open(f"{name}.txt", "r") # Open file in read mode, to look at patterns.
    all_player_moves = [line.strip() for line in player_data.readlines()]
    player_data.close()
    return all_player_moves

def update_highest_chains(array1,array2,array3,last,current_chain,group): # Part of the get_favorite_and_highest_chains() module.
    if last == "1":
        if current_chain > array1[group]:
            array1[group] = current_chain
    if last == "2":
        if current_chain > array2[group]:
            array2[group] = current_chain
    if last == "3":
        if current_chain > array3[group]:
            array3[group] = current_chain
    return

def get_favorite_and_highest_chains(player_moves_list): # Calculates 2 values, favorite and highest chains. really long, break this down more?
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
            # Final chain finish
            update_highest_chains(highest_one_chains,highest_two_chains,highest_three_chains,last,current_chain,group)
        # Assign most frequent button
        if one_counter > two_counter and one_counter > three_counter:
            favorite_button[group] = 1
        elif two_counter > one_counter and two_counter > three_counter:
            favorite_button[group] = 2
        elif three_counter > one_counter and three_counter > two_counter:
            favorite_button[group] = 3
        else:
            favorite_button[group] = random.randint(1,3) # TEMPORARY!!! Fallback for tied favorite buttons, replace this and line 97 with a better solution
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
            most_chained_buttons[time] = random.randint(1,3) # TEMPORARY!!! Fallback if any chains are tied, replace later with something better SHI THIS FIXED IT
    
    return most_chained_buttons, favorite_button, highest_chains

def weight_and_predict_move(player_moves_list, last_choice): # Calls functions to get the data values, then weights, calculates and returns the move.
    if len(player_moves_list) < 5:
        move = random.randint(1,3) # TEMPORARY!!! Fallback if data insufficient, pure RNG. might update this later to use an average person playerdata. 
        return move
        
    # Count highest chain of each button pressed in a row.
    most_chained_buttons, favorite_button, highest_chains = get_favorite_and_highest_chains(player_moves_list)

    # -----DEBUG CODE!!!-----
    # print(f"RECENT: ") // unfinished, i got too lazy to write allat
    # print(f"OVERALL: ")

    # Guess logic, give each button RNG weight, 5% chance of mindless RNG. (Tweak this as you go)
    weights = [0,0,0] # button 1, 2, 3, remainder = TOTAL RNG
    
    # 1. Decide if player is random or predictable
    multiplier = 1
    for period in range (0,2):
        if period == 1:
            multiplier = 2
        if highest_chains[period] >= 5: # VERY PREDICTABLE, +10 weight to highest chain.
            weights[last_choice-1] += (15/3)*multiplier
        if highest_chains[period] <= 2: # VERY RANDOM, -5 weight to highest chain. 
            weights[last_choice-1] -= (15/3)*multiplier
        else: # Somewhat random, +5 weight to highest chain. 
            weights[last_choice-1] += (5/3)*multiplier
        
    # Note: (95 - 25 = 70, so total of others must be 70, so 5% random chance if very predictable, 15% middleground, 25% if very random)
    # Keep adjusting this as more variables get added (recency bias done, then pattern recognition eg. 1, 2, 3, 1, 2, 3, since that completely breaks the AI)
    favorite_weight_overall = 20/3
    chain_weight_recent = 100/3
    favorite_weight_recent = 40/3

    # Overall biggest chain and favorite
    overall_chained, overall_favorite = most_chained_buttons[0], favorite_button[0] 
    weights[overall_favorite - 1] += favorite_weight_overall # +6 2/3 for favorite button.

    # Recent biggest chain and favorite
    recent_chained, recent_favorite = most_chained_buttons[1], favorite_button[1]
    weights[recent_chained - 1] += chain_weight_recent # +33 1/3 for most chained button.
    weights[recent_favorite - 1] += favorite_weight_recent # +13 1/3 for favorite button.
    # Use assigned RNG weight
    # print(weights) # DEBUG CODE
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

def check_for_pattern(player_moves_list): # Unfinished, checks repeating patterns of button choices.
    last_3_moves = player_moves_list[:3]
    print(last_3_moves)
    return

def main(): # Main gameplay loop
    player_name = input("Enter your name: ") # Get player name
    if not os.path.exists(f"{player_name}.txt"):
        with open(f"{player_name}.txt","w") as file: # Check for existing save file, create if not found.
            file.close()
    # Start both scores as 0
    turns = 0 # Used to trigger pattern check
    ai_score = 0 
    player_score = 0
    last_choice = random.randint(1,3) # Start with a random last choice
    
    # Main gameplay loop, continues until AI/player reach 10 points.
    while ai_score != 10 and player_score != 10:
        player_data_for_write = open(f"{player_name}.txt", "a") # Open file in append mode, as to not overwrite data. 
        player_data_for_read = get_player_data(player_name)
        ai_prediction = weight_and_predict_move(player_data_for_read, last_choice)
        print(f"AI Score: {ai_score}    Player Score: {player_score}")
        player_move = int(input("Choose which button (1/2/3): ")) # Get player choice
        if player_move < 1 or player_move > 3:
            print("Invalid input. ") # Error handling
            return
        last_choice = player_move # Store current player choice to be used in next turn for AI.
        if player_move == 1 or player_move == 2 or player_move == 3:
            new_data = f"{str(player_move)}\n"
            player_data_for_write.write(new_data)
            player_data_for_write.close()
        else:
            return
        if player_move == ai_prediction:
            ai_score += 1
        else:
            player_score += 1
        os.system('cls')

    if ai_score == 10:
        print("Game over, I've won.")
    else:
        print("Bravo, you win.")
           
main()