# Documentation

This document explains how this game works.

---

## Game Overview

Player chooses between 3 buttons, AI predicts which one user will press based on previous patterns, user wins if AI fails to predict. AI wins if it predicts correctly. First to 10 points wins

AI predicts based off 3 factors, most chained choice, most frequent choice, and the last choice, a more random player = more random AI.

More factors are being added, RNG is being adjusted.

---

## File Handling

A text file named after the player stores every input of the player. The AI refers to this file to calculate the most likely button the player will next press, with RNG involved.

---

## Prediction logic

The program turns the entire text file into an array which is used for the prediction logic which is broken into several functions, it calls each of these functions and then weighs the buttons accordingly and assigns a range to each button, and to a wildcard guess, then rolls a number between 1-100. Depending on which range it falls into, it picks the button to guess and then returns it to the main function.

---
