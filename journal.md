# Connect4 Project Journal

This document will serve as a daily log for the Connect4 project, detailing progress, challenges, and decisions.

## Date: 2025-07-14

### Progress:
- Implemented the piece-dropping animation for both the player and the AI in the Pygame GUI.
- Debugged and fixed a visual layering issue where the falling piece was being hidden by the background, ensuring the animation is now visible and appears correctly behind the game board.

### Challenges:
- Understanding the correct order of drawing (blitting) surfaces in Pygame to achieve the desired visual effect of a piece falling into a slot.

### Decisions:
- Decided on the correct layering order for rendering: draw the static background, then the moving piece, and finally the foreground board overlay.

### Next Steps:
- Implement on-screen messages for win/draw conditions.
- Add a "Play Again" button to allow restarting the game after it concludes.


## Date: 2025-07-13

### Progress:
- Successfully implemented the full Minimax algorithm with Alpha-Beta Pruning in `minimax_ai.py`.
- Guided the implementation of the `_minimax` function, including the maximizer and minimizer logic.
- Corrected the recursive calls and argument passing to resolve potential `None` type errors.
- Refined the `find_best_move` function to be a clean, single entry point to the minimax search.
- The AI is now significantly more efficient and intelligent.

### Challenges:
- Understanding the correct flow of `alpha` and `beta` values.
- Debugging recursive function calls and ensuring the correct values were returned.
- Identifying why the function could potentially return `None` and fixing the control flow with an `if/else` structure.

### Decisions:
- Adopted the standard convention for the `_minimax` function signature: `(self, board, depth, alpha, beta, maximizing_player)`.
- Simplified `find_best_move` to trust the recursive `_minimax` function, making the code cleaner and more efficient.

### Next Steps:
- Begin Phase 3: GUI Development.

## Date: 2025-07-11

### Progress:
- Implemented the core recursive logic of the `_minimax` function in `minimax_ai.py`.
- Integrated the `MiniMaxAI` into `connect4_cli.py`, allowing Player vs. AI gameplay.
- Addressed and fixed infinite loop bug when invalid moves were attempted by either player or AI.
- Refined `find_best_move` to handle potential `None` returns from `_minimax` more robustly.

### Challenges:
- Ensuring correct recursive calls and parameter passing within `_minimax`.
- Debugging the interaction between `find_best_move` and `_minimax`.
- Resolving linter warnings related to potential `None` types in comparisons.
- Identifying and fixing the infinite loop caused by invalid moves not switching players.
- Understanding the computational complexity of Minimax at higher depths.

### Decisions:
- Confirmed the use of `float('inf')` and `-float('inf')` for initial `min_eval` and `max_eval` values.
- Decided to explicitly handle `None` returns from `_minimax` in `find_best_move` for robustness.
- Prioritized fixing the invalid move loop to ensure game stability.

### Next Steps:
- Implement Alpha-Beta Pruning in the `_minimax` function for performance optimization.
- Begin Phase 3: GUI Development.

## Date: 2025-07-10

### Progress:
- Updated `planner.md` to include Reinforcement Learning as a future enhancement.
- Renamed `ai.py` to `minimax_ai.py` for better specificity.
- Created the `MiniMaxAI` class in `minimax_ai.py`.
- Implemented `__init__` to store AI's `player_piece` and `level`.
- Implemented `get_valid_moves` to identify available columns for moves.
- Implemented `_simulate_move` to create temporary board states for move simulation.
- Implemented `_is_winner` to check for win conditions for any given piece.
- Implemented `_is_draw` to check for draw conditions.
- Implemented `_score_board` to evaluate terminal game states (win, loss, draw).
- Structured `find_best_move` to orchestrate the AI's decision-making using helper functions.

### Challenges:
- Ensuring correct deep copies of the game board for simulations.
- Debugging win condition checks (horizontal, vertical, diagonal).
- Understanding the flow of score propagation in Minimax.

### Decisions:
- Decided to use a `MiniMaxAI` class to encapsulate AI logic.
- Broke down complex AI logic into smaller, testable helper methods (`_simulate_move`, `_is_winner`, `_is_draw`, `_score_board`).
- Confirmed the use of `'   '` for empty cells based on `connect4_cli.py`.

### Next Steps:
- Implement the core recursive logic of the `_minimax` function, starting with its base case.
- Integrate Alpha-Beta Pruning into `_minimax` for optimization.

## Date: 2025-07-07

### Progress:
- Initial `GEMINI.md` file created and updated with project overview and Gemini's suggestions.
- `planner.md` and `journal.md` files created.
- Implemented the `Connect4` class with a fully functional `__init__` method.
- Successfully implemented and tested the `print_board` method, displaying the dynamic game board.

### Challenges:
- None yet, just getting started.

### Decisions:
- Decided to use Gemini CLI to guide the project development.
- Decided to start with a Command Line Interface (CLI) version of the game to focus on core logic.

### Progress:
- Successfully implemented and refined the `drop_piece` method, handling valid moves, full columns, and piece placement.

### Progress:
- Successfully implemented and refined the `check_win` method, covering all horizontal, vertical, and diagonal win conditions.
- Successfully implemented the `check_draw` method to detect full boards.
- Successfully implemented the `switch_player` method to alternate turns.
- Successfully implemented the `play_game` method, orchestrating the full CLI game flow.
- Integrated ANSI escape codes for colored player pieces in the terminal.

### Next Steps:
- Begin Phase 2: AI Integration, starting with AI Algorithm Selection.
