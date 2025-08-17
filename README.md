# Game Overview

Player and AI play rock paper scissors, AI tries to predict player's next move and plays corresponding move. Loser has to play russian roulette. 1 in 6 chance of taking damage. First to 0 HP loses.   
  
AI predicts next press based off of several factors, most chained choice, most frequent choice, last choice, etc. a more random player = more random AI.  
  
More factors are being added, RNG is being adjusted.  

---

## Functional Features

---

### File Handling

A text file named after the player stores every input of the player. The AI refers to this file to calculate the most likely button the player will next press, with RNG involved.  

---

## Russian Roulette

Rather than using a traditional first to X score, every time the player or AI loses, they try their luck in russian roulette, losing 1 health point if the gun fires. The player and AI HP varies on each difficulty.  
  
Planned HP:  
Practice mode: AI: 3, Player: 5  
Basic: AI: 3, Player: 3  
Unfair: AI: 3, Player: 1  
  
(1 in 6 chance of gun firing)  

---
### Prediction Logic (To be improved)

The program turns the entire text file into an array which is used for the prediction logic which is broken into several functions, it calls each of these functions and then weighs the buttons accordingly and assigns a range to each button, and to a wildcard guess, then rolls a number between 1-100. Depending on which range it falls into, it picks the button to guess and then returns it to the main function.

---

### Confidence Meter/Multiplier

Adaptive meter measuring AI's confidence. Starts at 1, increases/decreases by 0.1 when AI wins/loses. Capped at maximum 1.5x, minimum 0.5x. Basic but useful feature. Only enabled in hard mode. Confidence meter is absent in practice and basic mode, with the multiplier being set at a static value.

---

## Unfinished Features

Once all of these features are finished, the game will be complete, with only minor bug fixes or improvements:  
-Complex/simple pattern recognition [In progress]  
-Russian Roulette to replace FT10 system [Not implemented]  
-Change game to rock paper scissors [Not implemented]  
-Improved file management [Not implemented]  
-Graphics [Not implemented]  
-Audio/Sound effects [Not implemented]  
-Miscallaneous, fun mechanics (powerups, powerdowns eg) [Not implemented]  
-Challenge Mode: 1 HP, endless with invincible hardmode bot.  

---

### Pattern Recognition (Work in Progress)

The most "intelligent" part of this AI. Takes the last two turns of the user, then loops and reads through the move history, seeing if this ever was used, if it was, check the next input in sequence to this, and add a weight to it, which adapts to how many times it's been repeated. Detects patterns 2 moves or longer. Ran on each turn, stores patterns in a 2D array stored in function weight_and_predict_move(). For every button in the pattern the user has pressed, increases pattern_weight, max 30, so it's not TOO sure.  
  
Will add 2 versions, simple and complex. adds a bit of a difficulty setting to the bot.  

---
