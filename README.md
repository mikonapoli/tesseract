# Tesseract
A simple Tetris clone in Python


This is my attempt as developing, from scratch, a full Tetris clone implementing as much as possible the
Tetris Guideline (https://tetris.wiki/Tetris_Guideline)

This is my first attempt at a complete software project and my first goal is to have a full, playable game.
After that, I plan to use this to experiment with development practices, tools and languages I plan to explore.

So far, the following features have been implemented:

* Window and input manager
* Basic game logic: pieces can be moved, dropped and rotated (only clockwise, until I decide a key mapping, but the implementation 
the counter-clockwise rotation is basically there). All 7 tetriminoes are working correctly colored and lines are cleared when full.
* Full SRS (https://tetris.wiki/SRS) including the prescribed wall kicks
* Random Generator (https://tetris.wiki/Random_Generator)
* Next piece preview

## Key bindings:
At the moment, pieces are moved with left and right arrow, hard dropped with down arrow and rotated with the up arrow

## Requirements: 
The game is developed in Python 3 and requires the pysdl2 library (and SDL2, of course).
