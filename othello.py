# othello.py

# Import necessary libraries
import copy
import random
import tkinter as tk

# Define constants for player colors
EMPTY = 0
BLACK = 1
WHITE = 2

# Set up the initial game state
def initial_state():
    board = [[EMPTY] * 8 for _ in range(8)]
    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE
    return board

# Display the current state of the board
def draw_board(board):
    print("  a b c d e f g h")
    print(" +-+-+-+-+-+-+-+-+")
    for i in range(8):
        print("{}|".format(i+1), end="")
        for j in range(8):
            if board[i][j] == EMPTY:
                print(" |", end="")
            elif board[i][j] == BLACK:
                print("X|", end="")
            else:
                print("O|", end="")
        print("\n +-+-+-+-+-+-+-+-+")

# Check if a move is valid
def is_valid_move(board, row, col, color):
    # Check if the cell is empty
    if board[row][col] != EMPTY:
        return False

    # Check if there are any outflanked opponent's pieces
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8) or board[r][c] == color or board[r][c] == EMPTY:
                continue
            while True:
                r, c = r + dr, c + dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                if board[r][c] == EMPTY:
                    break
                if board[r][c] == color:
                    return True
    return False

# Make a move on the board
def make_move(board, row, col, color):
    board = copy.deepcopy(board)
    board[row][col] = color

    # Flip opponent's pieces
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8) or board[r][c] == color or board[r][c] == EMPTY:
                continue
            while True:
                r, c = r + dr, c + dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                if board[r][c] == EMPTY:
                    break
                if board[r][c] == color:
                    r, c = r - dr, c - dc
                    while board[r][c] != color:
                        board[r][c] = color
                        r, c = r - dr, c - dc
                    break
    return board

# Get valid moves for a player
def get_valid_moves(board, color):
    moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, color):
                moves.append((row, col))
    return moves

# Evaluate the current game state
def get_score(board, color):
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    return black_score - white_score if color == BLACK else white_score - black_score

# Implement alpha-beta pruning with minimax
def minimax(board, depth, alpha, beta, maximizing_player, color):
    if depth == 0 or len(get_valid_moves(board, color)) == 0:
        return get_score(board, color)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_valid_moves(board, color):
            new_board = make_move(board, move[0], move[1], color)
            eval = minimax(new_board, depth - 1, alpha, beta, False, color)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_valid_moves(board, 3 - color):  # 3 - color gives the opponent's color
            new_board = make_move(board, move[0], move[1], 3 - color)
            eval = minimax(new_board, depth - 1, alpha, beta, True, color)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Get the best move using alpha-beta pruning
def get_best_move(board, depth, color):
    best_move = None
    max_eval = float('-inf')
    for move in get_valid_moves(board, color):
        new_board = make_move(board, move[0], move[1], color)
        eval = minimax(new_board, depth - 1, float('-inf'), float('inf'), False, color)
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move

# Main function to play the game
def play_game():
    board = initial_state()
    current_color = BLACK

    while True:
        draw_board(board)
        if len(get_valid_moves(board, current_color)) == 0:
            print("No valid moves for {}. Passing the turn.".format("Black" if current_color == BLACK else "White"))
            current_color = 3 - current_color  # Switch player
            if len(get_valid_moves(board, current_color)) == 0:
                print("No more valid moves for either player. Game Over!")
                black_score = sum(row.count(BLACK) for row in board)
                white_score = sum(row.count(WHITE) for row in board)
                if black_score == white_score:
                    print("It's a tie!")
                elif black_score > white_score:
                    print("Black wins with a score of {}-{}!".format(black_score, white_score))
                else:
                    print("White wins with a score of {}-{}!".format(white_score, black_score))
                break
            continue
        if current_color == BLACK:
            print("Black's turn.")
            # Adjust depth based on difficulty level
            depth = 3  # Change this based on difficulty (Easy: 1, Medium: 3, Hard: 5)
            move = get_best_move(board, depth, BLACK)
            print("AI chose move:", chr(move[1] + ord('a')) + str(move[0] + 1))
        else:
            print("White's turn.")
            # Prompt the user for move
            while True:
                try:
                    move_input = input("Enter your move (e.g., a1): ")
                    col = ord(move_input[0].lower()) - ord('a')
                    row = int(move_input[1]) - 1
                    if not (0 <= row < 8 and 0 <= col < 8 and is_valid_move(board, row, col, WHITE)):
                        raise ValueError("Invalid move.")
                    break
                except ValueError:
                    print("Invalid input or move. Try again.")
            move = (row, col)
        board = make_move(board, move[0], move[1], current_color)
        current_color = 3 - current_color  # Switch player

# Run the game
if __name__ == "__main__":
    play_game()
