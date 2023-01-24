# import the sys library so that we can read from standard in.
import sys
# a function that prints out the board. It also prints our row and
# column numbers as appropriate.
def printBoard(array):
    for row in range(len(array)):
        print(f"{row}", end = " ")
    print()

    for row in range(len(array)):
        print(f"{row}", end = " ")
        for col in range(len(array[row])):
            print(f"{array[row][col]}", end = " ")
        print()

def copyboard(board):
    #create a new board
    newboard = []
    
    #for every row in the original matrix,
    #create a row in the new matrix
    for row in board:
        newboard.append([])
        
        #for every column value in the row, append to the new matrix
        for col in row:
            newboard[len(newboard)-1].append(col)
            
    return newboard

def computeNextGen(board):
    nextboard = copyboard(board)
    
    for row in range(1, size-1):
        for col in range(1, size-1):
            neighbors = countNeighbors(board, row, col)
            
            #Star dies if it has fewer than 2 or greater than 3 neighbors
            if(board[row][col] == "*"):
                if neighbors < 2 or neighbors > 3:
                    nextboard[row][col] = " "
                    
            #A star is created if an empty space has exactly 3 neighbors
            else:
                if neighbors == 3:
                    nextboard[row][col] = "*"
    return nextboard

#A function that counts the neighbors in the 8 spaces around a space on the board
def countNeighbors(board, row, col):
    neighbors = 0
    
    #for the row above, below and with the space
    for i in range(-1, 2):
        #for the column left, right and with the space
        for j in range(-1, 2):
            
            #if the space contains a star add to neighbors
            if not (i == 0 and j == 0):
                if board[row+i][col+j] == "*":
                    neighbors += 1
    return neighbors

# Initialize an empty array to store the contents of the file that we
# shall be reading.
board = []

# For each line in the file, create a new array in the board. For each
# character in the line, append that character to the appropriate array.
for line in sys.stdin:
    board.append([])
    size = len(line)-1
    for i in range(len(line)-1):
        board[len(board) - 1].append(line[i])

# print the board using our custom printboard function
printBoard(board)
while True:
    board = computeNextGen(board)
    printBoard(board)
