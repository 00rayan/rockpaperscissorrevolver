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

### Russian Roulette

Rather than using a traditional first to X score, every time the player or AI loses, they try their luck in russian roulette, losing 1 health point if the gun fires. The player and AI HP varies on each difficulty. Difference being, on easy mode, this is disabled and damage is just guaranteed.
  
Planned HP:  
Easy: AI: 3, Player: 5 
Standard: AI: 2, Player: 2  
Unfair: AI: 3, Player: 1  
  
There is a 1 in 3 chance of gun firing on easy and standard.  
  
UNFAIR MODE ONLY: There is a 1 in 6 chance of the revolver firing, HOWEVER, every (missed) shot taken, the chance increases, 1 in 5, 1 in 4, until the revolver is eventually fired. A tie also progresses the chamber for both sides similarly, albeit without firing.  

---
### Prediction Logic (To be improved)

The program turns the entire text file into an array which is used for the prediction logic which is broken into several functions, it calls each of these functions and then weighs the buttons accordingly and assigns a range to each button, and to a wildcard guess, then rolls a number between 1-100. Depending on which range it falls into, it picks the button to guess and then returns it to the main function.

---

### Win/lose based predictions

Alongside the function that reads the playerdata, number of wins, ties and losses are counted and stored in appropriate integer variables. Then, the next move in sequence for the file is checked, if it changes it is counted. The percentage of wins/losses/ties that result in the user changing their choice is calculated, and then according to this a weight is calculated which is either evenly distributed to every other choice except the last or added to the last choice.  
  
The formula for the weight is:  
  
        W = 5 + 0.3(C-50) 50 < C < 100  
        W = 5 + 0.3(50-C)  0 < C < 50  
  
---

### Confidence Meter/Multiplier

Adaptive meter measuring AI's confidence. Starts at 1, increases/decreases by 0.1 when AI wins/loses. Capped at maximum 1.5x, minimum 0.5x. Basic but useful feature. Only enabled in hard mode. Confidence meter is absent in easy and standard mode, with the multiplier being set at a static value.

---

## Unfinished Features

Once all of these features are finished, the game will be complete, with only minor bug fixes or improvements:  

-Graphics [Functional, needs to be polished]  
-Win/lose based predictions [Not implemented]  
-Dynamic weighting [In progress]
-Simple pattern recognition [Done]
-Russian Roulette to replace FT10 system [Done]  
-Change game to rock paper scissors [Done]  
-Improved file management [Not implemented]  
-Audio/Sound effects [Not implemented]  
-Miscallaneous, fun mechanics (powerups, powerdowns eg) [Not implemented]  
-Challenge Mode: 1 HP, endless with invincible hardmode bot. [Not implemented]  
-Complex pattern recognition [Scrapped]  

Development Stages:
1. Make first finished prototype with graphics [Done]  
2. Significantly improve AI [In progress]  
3. Polish visuals, animations, SFX, etc. [Not started]  

---

### Pattern Recognition (Work in Progress)

The most "intelligent" part of this AI. Takes the last two turns of the user, then loops and reads through the move history, seeing if this ever was used, if it was, check the next input in sequence to this, and add a weight to it, which adapts to how many times it's been repeated. Detects patterns 2 moves or longer. Ran on each turn, stores patterns in a 2D array stored in function weight_and_predict_move(). For every button in the pattern the user has pressed, increases pattern_weight, max 30, so it's not TOO sure.  
  
Will add 2 versions, simple and complex. adds a bit of a difficulty setting to the bot.  

---
