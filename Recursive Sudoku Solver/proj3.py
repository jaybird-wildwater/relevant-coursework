# File:    proj3.py
# Author:  Julia Nau
# Date:    12/8/18
# Section: 19
# E-mail:  jnau1@umbc.edu
# Description:
#     Solve, and allow the user to solve, a sudoku puzzle.

GAME_MENU = ["p", "s"]
GAME_MSG = "Play (p) or solve (s)? "
CHECK_MENU = ["y", "n"]
CHECK_MSG = "Correctness checking? (y/n): "
PLAY_MENU = ["p", "u", "s", "q"]
PLAY_MSG = "Play number (p), save (s), undo (u), quit (q): "

NONET_LIST_1 = [0, 1, 2]
NONET_LIST_2 = [3, 4, 5]
NONET_LIST_3 = [6, 7, 8]

# getNonet() creates a 2d list containing the vertical and horizontal
#            range of the appropriate nonet
# Input:     row; the row being considered
#            column; the column being considered
# Output:    nonet; the 2d list of the nonet's ranges
def getNonet(row, column):
    # Initialize the empty nonet list
    nonet = []
    # Append the first list: the vertical range
    if row in NONET_LIST_1:
        nonet.append(NONET_LIST_1)
    elif row in NONET_LIST_2:
        nonet.append(NONET_LIST_2)
    elif row in NONET_LIST_3:
        nonet.append(NONET_LIST_3)

    # Append the second list: the horizontal range
    if column in NONET_LIST_1:
        nonet.append(NONET_LIST_1)
    elif column in NONET_LIST_2:
        nonet.append(NONET_LIST_2)
    elif column in NONET_LIST_3:
        nonet.append(NONET_LIST_3)

    return nonet

# validateOptions() makes sure that the user's choice is valid
# Input:            menu; a list of valid options
#                   msg; a string used for the input statements
# Output:           choice; the validated choice
def validateOptions(menu, msg):
    choice = input(msg)
    while choice not in menu:
        choice = input(msg)
    return choice

# validateDim() makes sure that the dimension (row or column) is valid
# Input:        dimension; "row" or "column" (for print statement)
# Output:       the validated dimension
def validateDim(dimension):
    msg = "Enter a " + dimension + " (1-9): "
    num = int(input(msg))
    while num < 1 or num > 9:
        print("Your value must be between 1 and 9.")
        num = int(input(msg))
    return num - 1

# validateNum() makes sure that the number to be played is valid
# Input:        row; the row being considered (for print statement)
#               column; the column being considered (for print statement)
# Output:       num; the validated number to be played
def validateNum(row, column):
    msg = "Enter a number to place in cell (" + str(row+1) + ", " + \
        str(column+1) + "): "
    num = int(input(msg))
    while num < 1 or num > 9:
        print("Your value must be between 1 and 9.")
        num = int(input(msg))
    return num

# validateMove() checks if the attempted move complies with the rules of
#                Sudoku
# Input:         row; the row being considered
#                column; the column being considered
#                number; the number to be placed in the cell
#                board; the gameboard
# Output:        valid; whether or not the move is valid
def validateMove(row, column, number, board):
    valid = True
    # If the cell is already full, move is not valid
    if board[row][column] != 0:
        print()
        valid = False
        print("There's already a number in that cell! Try again.")
    # If the row already contains number, move is not valid
    for i in range(len(board)):
        if board[i][column] == number:
            valid = False
            print("The number", number, "is already in that column.")
    # If the column already contains number, move is not valid
    for j in range(len(board[row])):
        if board[row][j] == number:
            valid = False
            print("The number", number, "is already in that row.")
    nonet = getNonet(row, column)
    # Get nonet. If the nonet already contains number, move is not valid
    for k in range(3):
        for l in range(3):
            if board[nonet[0][k]][nonet[1][l]] == number:
                valid = False
                print("The number", number, "is already in that square.")
    if valid == False:
        return False
    return True

# handleMove() checks if the attempted move complies with the rules of
#              Sudoku, and handles it if so
# Input:       board; the gameboard
#              rows; the list of moves' rows, listed chronologically
#              columns; the list of moves' columns, listed chronologically
# Output:      valid; whether or not the move is valid
def handleMove(board, rows, columns):
    # First, get and validate all three components of the move
    row = validateDim("row")
    column = validateDim("column")
    number = validateNum(row, column)
    # Check if the move is valid
    valid = validateMove(row, column, number, board)
    # If valid, update the board, rows and columns
    if valid:
        board[row][column] = number
        rows.append(row)
        columns.append(column)
    return valid

# check() compares the attempted move with the solution, and does not allow
#         incorrect moves to be played
# Input:  board; the gameboard
#         rows; the list of moves' rows, listed chronologically
#         columns; the list of moves' columns, listed chronologically
#         solution; the solved gameboard
# Output: whether or not the move is correct
def check(board, rows, columns, solution):
    # First, get and validate all three components of the move
    row = validateDim("row")
    column = validateDim("column")
    number = validateNum(row, column)
    # Check if the move is correct. If so update the board, rows and columns
    if solution[row][column] == number:
        board[row][column] = number
        rows.append(row)
        columns.append(column)
        return True
    # If not correct, say so
    else:
        print()
        print("OOPS!", number, "does not belong in position (" + str(row+1)\
              + ", " + str(column+1) + ")!")
        return False

# undo()  undoes the last valid move
# Input:  board; the gameboard
#         rows; the list of moves' rows, listed chronologically
#         column; the list of the moves' columns, listed chronologically
# Output: None; updates the board and two lists
def undo(board, rows, columns):
    # If there are no moves left not-undid, say so.
    if rows == []:
        print("There are no moves to undo!")
    # Replaces the most recently-updated cell with a zero (rows and columns
    # are updated in main()
    else:
        # Four lines of code just for one print statement! #
        print("Removed the", \
              str(board[rows[(len(rows)-1)]][columns[(len(columns)-1)]]), \
              "you placed at position (" + str(rows[(len(rows)-1)]+1) +\
              ", " + str(columns[(len(columns)-1)]+1) + ").")
        board[rows[(len(rows)-1)]][columns[(len(columns)-1)]] = 0

# validateMoveSolve() does the same thing as validateMove(), but without
#                     any flavor text printouts
# Input:              row; the row being considered
#                     column; the column being considered
#                     number; the number to be placed in the cell
#                     board; the gameboard
# Output:             valid; whether or not the move is valid
def validateMoveSolve(row, column, number, board):
    valid = True
    # If the cell is already full, move is not valid
    if board[row][column] != 0:
        valid = False
    # If the row already contains number, move is not valid
    for i in range(len(board)):
        if board[i][column] == number:
            valid = False
    # If the column already contains number, move is not valid
    for j in range(len(board[row])):
        if board[row][j] == number:
            valid = False
    # Get nonet. If the nonet already contains number, move is not valid.
    nonet = getNonet(row, column)
    for k in range(3):
        for l in range(3):
            if board[nonet[0][k]][nonet[1][l]] == number:
                valid = False
    return valid

# convertPuzzle() reads in a puzzle from a file and converts it to a
#                 useful format
# Input:          fileName; the file to be converted
# Output:         board; the converted puzzle
def convertPuzzle(fileName):
    # Open the file and read its lines into a list, board
    fileName = open(fileName, "r")
    lines = fileName.readlines()
    board = []
    # .strip and .split by commas each line, and cast each value to an int
    for i in range(len(lines)):
        line = lines[i].strip()
        line = line.split(",")
        for j in range(len(line)):
            line[j] = int(line[j])
        board.append(line)
    # Close the file (it won't be used again)
    fileName.close()
    return board

# jDeepCopy() makes a deep copy of a given board
# Input:      board; the board to be copied
# Output:     boardCopy; a deep copy of the board
def jDeepCopy(board):
    boardCopy = []
    # For each cell, place its value in the same cell in boardCopy
    for i in range(len(board)):
        newRow = []
        for j in range(len(board[i])):
            newRow.append(board[i][j])
        boardCopy.append(newRow)
    return boardCopy

# getSolution() recursively computes the answer to a given sudoku puzzle,
#               and saves that solution to use for comparisons later on
#               (through updating a deep-copied puzzle board)
# Input:        board; the square 2d game board (of integers) to solve
#               row; the row being dealt with
#               column; the column being dealt with
#               left; the number of empty squares left
# Output:       none; updates the solution board
def getSolution(board, row, column, left):

    # Prepare row and column numbers for the next recursive call
    newRow = row
    newColumn = column + 1
    if newColumn > len(board)-1:
        newColumn = 0
        newRow += 1

    # If all squares are filled, the function is finshed
    if left == 0:
        return True
    # If the current cell is already filled, skip to the next cell
    elif board[row][column] != 0:
        return getSolution(board, newRow, newColumn, left)
    # Else, check whether each number (1-9) fits in the cell. If so, move
    # on to the next cell. If nothing fits, return to the previous cell
    else:
        for i in range(1, len(board)+1):
            if validateMoveSolve(row, column, i, board) == True:
                board[row][column] = i
                if getSolution(board, newRow, newColumn, left-1) == True:
                    return True
                board[row][column] = 0
        return False

# prettyPrint() prints the board with row and column labels,
#               and spaces the board out so that it looks nice
# Input:        board;   the square 2d game board (of integers) to print
# Output:       None;    prints the board in a pretty way
def prettyPrint(board):
    # print column headings and top border
    print("\n    1 2 3 | 4 5 6 | 7 8 9 ") 
    print("  +-------+-------+-------+")

    for i in range(len(board)): 
        # convert "0" cells to underscores  (DEEP COPY!!!)
        boardRow = list(board[i]) 
        for j in range(len(boardRow)):
            if boardRow[j] == 0:
                boardRow[j] = "_"

        # fill in the row with the numbers from the board
        print( "{} | {} {} {} | {} {} {} | {} {} {} |".format(i + 1, 
                boardRow[0], boardRow[1], boardRow[2], 
                boardRow[3], boardRow[4], boardRow[5], 
                boardRow[6], boardRow[7], boardRow[8]) )

        # the middle and last borders of the board
        if (i + 1) % 3 == 0:
            print("  +-------+-------+-------+")

            
# savePuzzle() writes the contents a sudoku puzzle out
#              to a file in comma separated format
# Input:       board; the square 2d puzzle (of integers) to write to a file
#              fileName; the name of the file to use for writing to 
def savePuzzle(board, fileName):
    ofp = open(fileName, "w")
    for i in range(len(board)):
        rowStr = ""
        for j in range(len(board[i])):
            rowStr += str(board[i][j]) + ","
        # don't write the last comma to the file
        ofp.write(rowStr[ : len(rowStr)-1] + "\n")
    ofp.close()


def main():
    # Initiate move-saving lists for use with undo()
    rows = []
    columns = []

    # Get and convert the puzzle file, and make a copy for the solution
    puzzleFile = input("Enter the file name for the Sudoku Puzzle: ")
    puzzle = convertPuzzle(puzzleFile)
    solution = jDeepCopy(puzzle)
    prettyPrint(jDeepCopy(puzzle))

    # Get gamemode
    mode = validateOptions(GAME_MENU, GAME_MSG)

    # Calculate number of empty spaces in the puzzle, and solve it
    zeroes = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                zeroes += 1
    getSolution(solution, 0, 0, zeroes)

    # If gamemode is solve, print the solution and skip playing the game
    if mode == "s":
        prettyPrint(solution)

    # If gamemode is play, get correctness checking mode and then loop
    # until the puzzle is solved
    elif mode == "p":
        cc = validateOptions(CHECK_MENU, CHECK_MSG)
        while zeroes > 0:

            # Get the player's move
            move = validateOptions(PLAY_MENU, PLAY_MSG)

            # If player chooses to make a move, either check or validate
            # the move, and reduce number of zeroes left
            if move == "p":
                if cc == "y":
                    valid = check(puzzle, rows, columns, solution)
                elif cc == "n":
                    valid = handleMove(puzzle, rows, columns)
                if valid:
                    zeroes -= 1
                    
            # If the player chooses to undo, undo() the last move and
            # increase the number of zeroes left
            elif move == "u":
                undo(puzzle, rows, columns)
                zeroes += 1
                rows = rows[:(len(rows)-1)]
                columns = columns[:(len(columns)-1)]

            # If the player chooses to save the puzzle, do so
            elif move == "s":
                fileName = input("Enter the filename you want to save to: ")
                savePuzzle(puzzle, fileName)

            # If the player choose to quit, print the board and exit the
            # program
            elif move == "q":
                print("Good bye! Here is the final board:")
                prettyPrint(puzzle)
                return
            
            # Print the puzzle after each move
            prettyPrint(jDeepCopy(puzzle))

        # When the game is over, print message and quit
        print("You win!")
        print()

        
main()
