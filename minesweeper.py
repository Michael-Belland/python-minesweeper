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

class Board:

    def __init__(self, numRows, numColumns, numMines):
        self.numRows = numRows
        self.numColumns = numColumns
        self.numMines = numMines
        self.mines = set()
        self.gameOver = False

        self.stateBoard = self.makeNewBoard(self.numRows, self.numColumns)
        self.playerBoard = self.makeNewBoard(self.numRows, self.numColumns)

    def printState(self):
        print "This board has %(nR)d row(s), %(nC)d column(s), and %(nM)d mine(s)." % {"nR": self.numRows, "nC": self.numColumns, "nM": self.numMines}
        self.printBoard()

    """
    Check standard docstring procedure

    Example: rows = 2, cols = 3

    [[X, X, X], 
     [X, X, X]] 

    Make sure to take care with indices!
    Confusion from variables sharing names with instance variables?
    """
    def makeNewBoard(self, numRows, numColumns):
        newBoard = [0] * numRows
        for i in xrange(numRows):
            newBoard[i] = [0] * numColumns
        return newBoard

    #TODO: fix printBoard behavior so board always is rectangular
    #      (currently, mines displays as the three character 'M', 
    #       making different rows different lengths in the output.)
    def printBoard(self):
        toPrint = ""
        for rowNum in xrange(len(self.stateBoard)):
            if rowNum == 0: 
                lineToPrint = "["
            else:
                lineToPrint = " "

            #lineToPrint += str(self.stateBoard[rowNum])
            lineToPrint += prettyPrintBasicList(self.stateBoard[rowNum])

            if rowNum < len(self.stateBoard) - 1: 
                lineToPrint += ", \n"
            else:
                lineToPrint += "]"

            #no real reason to individually add lineToPrint,
            #rather than directly add to toPrint, but useful
            #if we ever wanted something with individual lines
            toPrint += lineToPrint
        print toPrint

    def populateMines(self):
        #as a precaution, clear mines before generating new ones
        self.mines = set()
        self.stateBoard = self.makeNewBoard(self.numRows, self.numColumns)

        if self.numRows*self.numColumns < self.numMines:
            print "Error: too many mines to fit in board."

        while len(self.mines) < self.numMines:
            i = randint(0, self.numRows-1)
            j = randint(0, self.numColumns-1)
            if (i,j) not in self.mines:
                self.mines.add((i,j))
                self.stateBoard[i][j] = "M"




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


#game loop here; keep accepting inputs until game finished
#while not gameBoard.gameOver():
#    gameBoard.step()

print "Program execution complete."

#testing ideas:
#invalid inputs for board size or mine count
#  - what if these inputs aren't numbers?
#  - what if there are too many mines (numMines > numRows * numColumns)?