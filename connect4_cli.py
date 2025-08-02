import numpy as np

from minimax_ai import MiniMaxAI

class Connect4:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [['   ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = '\033[31m o \033[0m' # Red 'o'
        self.game_over = False


    def print_board(self):
        cell = "---+"
        horizontal_line = "+---+" + (self.cols-1) * cell
        col_num_string = "   ".join(str(i) for i in range(self.cols))

        #print board
        print(horizontal_line )

        for row in self.board:
            print('|' + '|'.join(row) + '|')

        print(horizontal_line )
        print("  " + col_num_string + "  ")

    def get_next_open_row(self, col):
        """
        Returns the next open row in the given column, or None if the column is full.
        Does NOT modify the board.
        """
        if col not in range(self.cols) or self.board[0][col] != '   ':
            return None
        
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == '   ':
                return row


    def drop_piece(self, col):
        # Verify move
        if col not in range(self.cols) or self.board[0][col] != '   ':
            # Print error
            print("Invalid move!!")
            return False, None
        
        # Drop piece to lowest row
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == '   ':
                self.board[row][col] = self.current_player
                return True, row
            
        return False, None
    
    def check_win(self):

        # Horizontal Win Condition
        for row in range(self.rows):
            for col in range(self.cols - 3): # -3: as u only need to check 4 consec. cols
                if self.board[row][col]   == self.current_player and \
                   self.board[row][col+1] == self.current_player and \
                   self.board[row][col+2] == self.current_player and \
                   self.board[row][col+3] == self.current_player:
                    return True
        
        # Vertical Win Condition
        for col in range(self.cols):
            for row in range(self.rows - 3): # -3: as u only need to check 4 consec. cols
                if self.board[row][col]   == self.current_player and \
                   self.board[row+1][col] == self.current_player and \
                   self.board[row+2][col] == self.current_player and \
                   self.board[row+3][col] == self.current_player:
                    return True        

        # Diagonal (/) Win Condition
        for col in range(self.cols - 3): 
            for row in range(self.rows-1, self.rows-4, -1):
                if self.board[row][col]   == self.current_player and \
                   self.board[row-1][col+1] == self.current_player and \
                   self.board[row-2][col+2] == self.current_player and \
                   self.board[row-3][col+3] == self.current_player:
                    return True            

        # Diagonal (\) Win Condition
        for col in range(self.cols - 3): 
            for row in range(self.rows - 3):
                if self.board[row][col]   == self.current_player and \
                   self.board[row+1][col+1] == self.current_player and \
                   self.board[row+2][col+2] == self.current_player and \
                   self.board[row+3][col+3] == self.current_player:
                    return True            
        return False
    
    def check_draw(self):
        for r in range(self.rows):
           for c in range(self.cols):
               if self.board[r][c] == '   ':
                   return False
        return True
    
    def switch_player(self):
        P1 = '\033[31m o \033[0m' # Red o
        P2 = '\033[34m o \033[0m' # Blue o

        if self.current_player == P1:
            self.current_player = P2
        
        else:
            self.current_player = P1

    def play_game(self):
        # --- Game Mode Selection ---
        game_mode = ''
        while game_mode not in ['1', '2']:
            game_mode = input("Choose game mode: (1) Player vs Player or (2) Player vs AI: ")

        ai_player = None
        if game_mode == '2':
            # AI will be Player 2, the blue piece
            ai_player = MiniMaxAI(player_piece='\033[34m o \033[0m', level=4)
            print("You are Player 1 \033[31m o \033[0m. The AI is Player 2 \033[34m o \033[0m.")

        # --- Start Game ---
        self.print_board()

        while not self.game_over:

            if ai_player is not None and self.current_player == '\033[34m o \033[0m':
                chosen_col = ai_player.find_best_move(self.board)

            else:
                try:
                    input_col = input(f"{self.current_player}'s move, , enter column (0-{self.cols-1}): ")
                    chosen_col = int(input_col)


                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue


            # 3. Attempt to execute move
            is_valid_move = self.drop_piece(chosen_col)

            # 3A. If move is valid: check win/draw then switch player
            if is_valid_move:
                self.print_board() # Display updated board after move

                if self.check_win():
                    print(f"{self.current_player} wins! :)")
                    self.game_over = True
                
                elif self.check_draw():
                    print("It's a draw! :|")
                    self.game_over = True

                else:
                    self.switch_player()

            else:
                continue


if __name__ == "__main__":
    game = Connect4()
    game.play_game() 
