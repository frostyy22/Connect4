from random import choice

class MiniMaxAI:

    def __init__(self, player_piece, level=4):
        self.player_piece = player_piece
        self.level = level
        if self.player_piece == '\033[31m o \033[0m':
            self.opponent_piece = '\033[34m o \033[0m'
        else:
            self.opponent_piece = '\033[31m o \033[0m'

        self.WIN_SCORE = 1000
        self.THREE_IN_A_ROW_SCORE = 100
        self.TWO_IN_A_ROW_SCORE = 10

    def get_valid_moves(self, board):
        valid_cols = []
        for col in range(len(board[0])):
            if board[0][col] == '   ':
                valid_cols.append(col)
        return valid_cols

    def _simulate_move(self, board, col, piece):
        temp_board = [row[:] for row in board]
        for row in range(len(temp_board) - 1, -1, -1):
            if temp_board[row][col] == '   ':
                temp_board[row][col] = piece
                return temp_board
        return None

    def _is_winner(self, board, piece):
        # Horizontal Win
        for row in range(len(board)):
            for col in range(len(board[0]) - 3):
                if all(board[row][col+i] == piece for i in range(4)):
                    return True
        # Vertical Win
        for col in range(len(board[0])):
            for row in range(len(board) - 3):
                if all(board[row+i][col] == piece for i in range(4)):
                    return True
        # Diagonal (/) Win
        for col in range(len(board[0]) - 3):
            for row in range(len(board) - 1, 2, -1):
                if all(board[row-i][col+i] == piece for i in range(4)):
                    return True
        # Diagonal (\) Win
        for col in range(len(board[0]) - 3):
            for row in range(len(board) - 3):
                if all(board[row+i][col+i] == piece for i in range(4)):
                    return True
        return False

    def _is_draw(self, board):
        return all(board[0][c] != '   ' for c in range(len(board[0])))

    def _score_board(self, board):
        if self._is_winner(board, self.player_piece):
            return 1000000
        elif self._is_winner(board, self.opponent_piece):
            return -1000000
        elif self._is_draw(board):
            return 0
        else:
            # This is a non-terminal state
            return None
        
    def _evaluate_window(self, window, piece):
        score = 0

        if piece == self.player_piece:
            opp_piece = self.opponent_piece
        else:
            opp_piece = self.player_piece
    
        if window.count(piece) == 4:
            score += self.WIN_SCORE

        elif window.count(piece) == 3 and window.count('   ') == 1 :
            score += self.THREE_IN_A_ROW_SCORE

        elif window.count(piece) == 2 and window.count('   ') == 2 :
            score += self.TWO_IN_A_ROW_SCORE

        if  window.count(opp_piece) == 3 and window.count('   ') == 1 :
            score -= self.THREE_IN_A_ROW_SCORE   

        elif window.count(opp_piece) == 4:
            score -= self.WIN_SCORE 
        
        return score


    def _heuristic_score(self, board, piece):
        score = 0

        # Horizontal Window
        for row in range(len(board)):
            for col in range(len(board[0]) - 3):
                window = [board[row][col+i] for i in range(4)]
                score += self._evaluate_window(window, piece)
        
        # Vertical Window
        for col in range(len(board[0])):
            for row in range(len(board) - 3):
                window = [board[row + i][col] for i in range(4)]
                score += self._evaluate_window(window, piece)

        # Diagonal (/) Window
        for col in range(len(board[0]) - 3):
            for row in range(len(board) - 1, 2, -1):      
                window = [board[row-i][col+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        # Diagonal (\) Window
        for col in range(len(board[0]) - 3):
            for row in range(len(board) - 3):
                window = [board[row+i][col+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        return score


    def _minimax(self, board, depth, maximizing_player, alpha, beta):
        # --- Base Cases ---
        score = self._score_board(board)
        if score is not None: # If board is not in an end state 
            return (None, score)      
        if depth == 0:        # Check if we've reached the maximum depth
            return (None, self._heuristic_score(board, self.player_piece))
        
        
        # --- Recursive Step ---
        #--------   AI   --------
        if maximizing_player:
            max_eval = -float('inf')
            valid_moves = self.get_valid_moves(board)
            best_move = choice(valid_moves) # Start with a random column

            for move in valid_moves:
                #Updated board after a simul. move
                temp_board = self._simulate_move(board, move, self.player_piece)

                evaluation = self._minimax(temp_board, depth-1, not maximizing_player, alpha, beta)[1]

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                
                alpha = max(max_eval, alpha)

                if alpha >= beta:
                    break
            
            return best_move, max_eval

        #-------- PLAYER --------        
        else:
            min_eval = float('inf')
            valid_moves = self.get_valid_moves(board)
            best_move = choice(valid_moves) # Start with a random column

            for move in valid_moves:
                #Updated board after a simul. move
                temp_board = self._simulate_move(board, move, self.opponent_piece)
                
                evaluation = self._minimax(temp_board, depth-1, not maximizing_player, alpha, beta)[1]

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                
                beta = min(min_eval, beta)

                if alpha >= beta:
                    break
            
            return best_move, min_eval

    def find_best_move(self, board):
        best_col, minimax_score = self._minimax(board, self.level, True, -float('inf'), float('inf'))

        return best_col
 