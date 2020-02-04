from random import randint

#TODO: this is pretty similar to what prints the row list in Board.printBoard...
#      can we consolidate the two functions into one?
#      The inputs differ (Board.printBoard is a list of lists, while this is a
#      list of strings), so it's not as simple as having different function signatures
def prettyPrintBasicList(inputList):
    toReturn = "["
    listIndex = 0

    #print all elements of the list except the last one, which is special cased
    while listIndex < len(inputList) - 1:
        toReturn = toReturn + str(inputList[listIndex]) + ", "
        listIndex += 1

    #print the last element of the list, assuming the list was non-empty
    if len(inputList) > 0:
        toReturn = toReturn + str(inputList[-1])
    toReturn = toReturn + "]"

    return toReturn

#The player's coordinate system will be like a typical x-y graph:
#The bottom-left is 0,0, and increasing those numbers moves to the top right.
class Board:

    def __init__(self, numRows, numColumns, numMines):
        self.numRows = numRows
        self.numColumns = numColumns
        self.numMines = numMines
        self.mines = set()
        self.gameOver = False

        #Honestly, an object oriented approach (a 2d array of Cells, with subclassing)
        #would probably be more intuitive than this design.  But let's see where this goes.
        self.stateBoard = self.makeNewBoard(self.numRows, self.numColumns)
        self.playerBoard = self.makeNewBoard(self.numRows, self.numColumns, "#")

    def printState(self):
        print "This board has %(nR)d row(s), %(nC)d column(s), and %(nM)d mine(s)." % {"nR": self.numRows, "nC": self.numColumns, "nM": self.numMines}
        self.printBoard(self.stateBoard)
        self.printBoard(self.playerBoard)

    """
    Check standard docstring procedure

    Example: rows = 2, cols = 3

    [[X, X, X], 
     [X, X, X]] 

    Make sure to take care with indices!
    Confusion from variables sharing names with instance variables?
    """
    def makeNewBoard(self, numRows, numColumns, displayChar=0):
        newBoard = [0] * numRows
        for i in xrange(numRows):
            newBoard[i] = [displayChar] * numColumns
        return newBoard

    #TODO: fix printBoard behavior so board always is rectangular
    #      (currently, mines displays as the three character 'M', 
    #       making different rows different lengths in the output.)
    def printBoard(self, board):
        toPrint = ""
        for rowNum in xrange(len(board)):
            if rowNum == 0: 
                lineToPrint = "["
            else:
                lineToPrint = " "

            #lineToPrint += str(self.stateBoard[rowNum])
            lineToPrint += prettyPrintBasicList(board[rowNum])

            if rowNum < len(board) - 1: 
                lineToPrint += ", \n"
            else:
                lineToPrint += "]"

            #no real reason to individually add lineToPrint,
            #rather than directly add to toPrint, but useful
            #if we ever wanted something with individual lines
            toPrint += lineToPrint
        print toPrint

    #ignoredSpaceList squares are guaranteed to not have mines
    #this can be helpful by, for example, preventing the first
    #square the user clicks from being a mine (populate mines after)
    def populateMines(self, ignoredSpaceList=[]):
        #as a precaution, clear mines before generating new ones
        self.mines = set()
        self.stateBoard = self.makeNewBoard(self.numRows, self.numColumns)
        self.playerBoard = self.makeNewBoard(self.numRows, self.numColumns, "#")

        if self.numRows*self.numColumns < self.numMines+len(ignoredSpaceList):
            print "Error: too many mines to fit in board."
            return

        while len(self.mines) < self.numMines+len(ignoredSpaceList):
            i = randint(0, self.numRows-1)
            j = randint(0, self.numColumns-1)
            if (i,j) not in self.mines and (i,j) not in ignoredSpaceList:
                self.mines.add((i,j))
                self.stateBoard[i][j] = "M"

        #next, go through the stateBoard to populate squares adjacent to mines with numbers
        #with oop implementation, go to each mine M -> find neighbors -> add *M to neighborMineList field (or increment a counter)
        #here, we'll just go through each square of the board and calculate the mine count separately.

        for j in xrange(self.numRows):
            for i in xrange(self.numColumns):
                if self.stateBoard[j][i] != "M":
                    neighbors = self.getNeighborSet(i, j)
                    a = lambda (x, y): self.stateBoard[y][x] == "M"
                    neighborMineCount = len(filter(lambda (x, y): self.stateBoard[y][x] == "M", neighbors))
                    self.stateBoard[j][i] = neighborMineCount

    #a player should only be able to flag a non-revealed square
    #a flagged square should not be revealed, even by other squares
    def playerToggleFlag(self, flagX, flagY):
        if self.playerBoard[-flagY-1][flagX] == "#":
            self.playerBoard[-flagY-1][flagX] = "F"
        elif self.playerBoard[-flagY-1][flagX] == "F":
            self.playerBoard[-flagY-1][flagX] = "#"

    def playerProbeSquare(self, probeX, probeY):
        if self.stateBoard[-flagY-1][flagX] == "M":
            print "You uncovered a mine!  Game over."
            #break the gameplay loop
        else:
            #TODO: if 0 square, uncover neighbors
            #      if F square, ignore
            #      otherwise, uncover square and stop
            return

    #convenience function for finding squares adjacent to inputted square
    #the convenience comes in because it handles edge cases (literally)
    def getNeighborSet(self, squareX, squareY):
        neighbors = set()

        if squareY - 1 >= 0:
            neighbors.add((squareX, squareY-1))

        if squareY + 1 < numRows:
            neighbors.add((squareX, squareY+1))

        if squareX - 1 >= 0: 
            neighbors.add((squareX-1, squareY))

            if squareY - 1 >= 0:
                neighbors.add((squareX-1, squareY-1))

            if squareY + 1 < numRows:
                neighbors.add((squareX-1, squareY+1))

        if squareX + 1 < numColumns:
            neighbors.add((squareX+1, squareY))

            if squareY - 1 >= 0:
                neighbors.add((squareX+1, squareY-1))

            if squareY + 1 < numRows:
                neighbors.add((squareX+1, squareY+1))

        return neighbors











#if using imports, this would be main.py
#initialize the board
numRows = input("How many rows in the board? ")
numColumns = input("How many columns in the board? ")
numMines = input("How many mines in the board? ")

gameBoard = Board(numRows, numColumns, numMines)
gameBoard.printState()


#TODO: replace input with a function that sanitizes input first
#a = input("Press any key to continue to next test: populating mines.")
gameBoard.populateMines()
gameBoard.printState()

#inputX = input("Add a flag at X=")
#inputY = input("Add a flag at Y=")
#gameBoard.playerAddFlag(inputX, inputY)
#gameBoard.printState()


#game loop here; keep accepting inputs until game finished
#while not gameBoard.gameOver():
#    gameBoard.step()

print "Program execution complete."

#testing ideas:
#invalid inputs for board size or mine count
#  - what if these inputs aren't numbers?
#  - what if there are too many mines (numMines > numRows * numColumns)?