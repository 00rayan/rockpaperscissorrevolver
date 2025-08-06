# Game Overview

Player chooses between 3 buttons, AI predicts which one the player will press based on previous patterns, player wins if AI fails to predict button pressed. AI wins if it predicts correctly. First one to 10 points wins.

AI predicts next press based off of several factors, most chained choice, most frequent choice, last choice, etc. a more random player = more random AI.

More factors are being added, RNG is being adjusted.

---

## Functional Features

---

### File Handling

A text file named after the player stores every input of the player. The AI refers to this file to calculate the most likely button the player will next press, with RNG involved.

---

### Prediction Logic (To be improved)

The program turns the entire text file into an array which is used for the prediction logic which is broken into several functions, it calls each of these functions and then weighs the buttons accordingly and assigns a range to each button, and to a wildcard guess, then rolls a number between 1-100. Depending on which range it falls into, it picks the button to guess and then returns it to the main function.

---

## Unfinished Features

---

### Pattern Recognition (Work in Progress)

The most "intelligent" part of this AI. Takes the last two turns of the user, then loops and reads through the move history, seeing if this ever was used, if it was, check the next input in sequence to this, and add a weight to it, which adapts to how many times it's been repeated.

---

### Confidence Meter (Not added yet)

Adaptive meter which affects the entire weighting system; a multiplier on top of all weights. Increases when AI scores more points, decreases when it loses more points. Exponential(?). Kind of an adaptive difficulty setting so AI becomes more predictable and overconfident when it's winning, making an opening for the user to take advantage of it. However, when it's losing, it gets more frustrated and applies a negative multiplier to the weights, decreasing them and making the AI more random and uncalculated, possibly giving it the advantage.

---