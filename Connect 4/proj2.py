# File:    proj2.py
# Author:  Julia Nau
# Date:    11/8/18
# Section: 19
# E-mail:  jnau1@umbc.edu
# Description:
#     Play a game of Connect Four, with two players or vs the computer.

# Import randint() for computer's move
from random import randint, seed

# Constants for symbols
EMPTY_SPACE = "_"
X = "x"
O = "o"

# Constant for board size
MIN_SIZE = 5

# Constant for win condition
IN_A_ROW = 4

# Constants for dimensions
HEIGHT = "height"
WIDTH = "width"

# Constants for questions
COMPUTER = "computerFlag"
REMATCH = "rematchFlag"

# Constants for yes/no answers
YES = "y"
NO = "n"

# verify_size(dimension) compares a requested board dimension to MIN_SIZE
# Input:  dimension, a string used in the input message
# Output: validated size
def verify_size(dimension):

    msg = "Please enter the " + dimension + " of your board: "
    size = int(input(msg))

    while size < MIN_SIZE:
        size = int(input("Value must be at least 5. "))
    return size

# verify_yesno(question) ensures that the user has answered "y" or "n"
# Input:  question, a string to determine the input message
# Output: validated answer (y/n)
def verify_yesno(question):

    if question == COMPUTER:
        string = input("Would you like to play against the computer?(y/n) ")
    elif question == REMATCH:
        string = input("Would you like to play again?(y/n) ")

    while string != "y" and string != "n":
        string = input("Please enter either \"y\" or \"n\". ")
    return string

# verify_column(board) ensures that the requested column exists
# Input:  board, the gameboard
# Output: validated column
def verify_column(board):

    column = int(input("Choose a column for your next piece: "))

    while column < 1 or column > len(board[0]):
        column = int(input("Please enter a valid column."))
    return column

# build_board(height, width) produces a board of user-specified size
# Input:  requested width and height of the board
# Output: 2D list of EMPTY_SPACE symbols with desired dimensions
def build_board(height, width):

    boardHeight = 0
    board = []

    while boardHeight < height:
        boardWidth = 0
        row = []
        while boardWidth < width:
            row.append(EMPTY_SPACE)
            boardWidth += 1
        board.append(row)
        boardHeight += 1
    return board

# print_board(board) prints out the current state of the gameboard list
# Input:  board, the gameboard
# Output: prints out the gameboard in a uniform-looking grid
def print_board(board):

    hndex = 0

    while hndex < len(board):
        wndex = 0
        while wndex < len(board[hndex]):
            print(board[hndex][wndex], end=" ")
            wndex += 1
        print()
        hndex += 1
    print()

# place_chip(board, symbol, column, cpu) places the appropriate symbol at
#                                        lowest EMPTY_SPACE in the board
# Input:  the gameboard, the current player, the desired column, and whether
#         the computer is playing this turn
# Output: updates the gameboard and returns the row the piece landed in
def place_chip(board, symbol, column, cpu):

    column -= 1
    hndex = len(board) - 1

    while hndex >= 0:
        if board[hndex][column] == "_":
            board[hndex][column] = symbol
            return hndex
        else:
            hndex -= 1
            
    # If you're trying to add to a column that's already full, pick again
    if cpu == YES:
        column = computer_move(board)
    else:
        column = \
            int(input("This column is full. Please choose another. "))
    return place_chip(board, symbol, column, cpu)

# computer_move(board) choose a column at random if the cpu is player 2
# Input:  current state of the board
# Output: chosen column
def computer_move(board):

    column = randint(1, len(board[0]))
    return column

# check_horizontal(board, player, row) checks whether four in a row
#                                      exist in a given row
# Input:  the gameboard, the current player, and the row of the player's
#         most recent piece
# Output: whether or not four in a row exist
def check_horizontal(board, player, row):

    score = 0
    wndex = 0
    
    while wndex < len(board[row]):
        if board[row][wndex] == player:
            score += 1
            if score == IN_A_ROW:
                return True
        else:
            score = 0
        wndex += 1
    return False

# check_vertical(board, player, column) checks whether four in a row
#                                       exist in a given column
# Input:  the gameboard, the current player, and the column of the player's
#         most recent piece
# Output: whether or not four in a row exist
def check_vertical(board, player, column):

    # Modify column to allow for proper indexing
    column = column - 1
    score = 0
    hndex = 0

    while hndex < len(board):
        if board[hndex][column] == player:
            score += 1
            if score == IN_A_ROW:
                return True
        else:
            score = 0
        hndex += 1
    return False

# check_diagonal_up(board, player, row, column) checks whether four in a row
#                                               exist on a given upward
#                                               diagonal
# Input:  the gameboard, the current player, and the row and column of the
#         player's most recent piece
# Output: whether or not four in a row exist
def check_diagonal_up(board, player, row, column):

    hndex = row
    wndex = column - 1
    score = 0

    # Backtrack from the given point down and to the left, until you
    # reach the edge of the board horizontally OR vertically
    while hndex < len(board)-1 and wndex > 0:
        hndex += 1
        wndex -= 1

    # Now check every space in the upward diagonal from that point
    while hndex > 0 and wndex < len(board[0]):
        if board[hndex][wndex] == player:
            score += 1
            if score == IN_A_ROW:
                return True
        else:
            score = 0
        hndex -= 1
        wndex += 1
    return False


# check_diagonal_down(board, player, row, column) checks whether four in a
#                                               row exist on a given
#                                               downward diagonal
# Input:  the gameboard, the current player, and the row and column of the
#         player's most recent piece
# Output: whether or not four in a row exist
def check_diagonal_down(board, player, row, column):

    hndex = row
    wndex = column - 1
    score = 0

    # Backtrack from the given point up and to the left (toward the origin)
    # until you reach the edge of the board horizontally or vertically
    while hndex > 0 and wndex > 0:
        hndex -= 1
        wndex -= 1

    # Now check every space in the downward diagonal from that point
    while hndex < len(board) and wndex < len(board[0]):
        if board[hndex][wndex] == player:
            score += 1
            if score == IN_A_ROW:
                return True
        else:
            score = 0
        hndex += 1
        wndex += 1
    return False

# switch(symbol) switches to the next player's turn based on the current
#                player
# Input:  the current player
# Output: the next player
def switch(symbol):
    if symbol == X:
        return O
    elif symbol == O:
        return X


def main():
    # Loop until the user decides not to play anymore
    rematch = YES
    while rematch == YES:

        # Initialize the board
        height = verify_size(HEIGHT)
        width = verify_size(WIDTH)
        board = build_board(height, width)
        print_board(board)

        # Ask whether the computer should take over player 2
        computer = verify_yesno(COMPUTER)

        # Initialize the current player and 'win' variable
        player = X
        winner = ""

        # Loop until someone gets 4, or the board is filled
        while winner == "" and EMPTY_SPACE in board[0]:

            # Choice of column, accounting for if the computer is playing
            if computer == YES and player == O:
                print("My turn!")
                column = computer_move(board)
            else:
                column = verify_column(board)

            # Update the board and return the row for win-check purposes
            row = place_chip(board, player, column, computer)
            print_board(board)

            # Check for four-in-a-row based on the last played piece
            horizontal = check_horizontal(board, player, row)
            vertical = check_vertical(board, player, column)
            diagonalDown = check_diagonal_down(board, player, row, column)
            diagonalUp = check_diagonal_up(board, player, row, column)
            
            if horizontal or vertical or diagonalDown or diagonalUp:
                winner = player
            player = switch(player)

        # If a player won (no tie), congratulate that player
        if winner != "":
            if player == O:
                print("Player 1 wins!")
            elif player == X:
                print("Player 2 wins!")

        else:
            print("A tie!")

        # Ask whether to play again; if not, say thank you and switch off
        rematch = verify_yesno(REMATCH)
        
    print()
    print("Thank you for playing!")
    print()

    
main()
