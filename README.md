# Connect4

A simple Connect4 game with a GUI and an AI opponent.

## Core Game

The game is a classic Connect 4, where the objective is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.

The core game logic is built in Python, with the game board represented as a 2D array. The game checks for win and draw conditions after each move.

The graphical user interface (GUI) is built using the Pygame library, providing a visual and interactive experience. The game features a retro-futuristic theme with glowing pieces.

The AI opponent uses the Minimax algorithm with alpha-beta pruning to determine the best move. The AI's difficulty can be adjusted by changing the search depth of the Minimax algorithm.

## Tech Stack

- Python
- Pygame

## How to Run

```bash
python connect4_gui.py
```