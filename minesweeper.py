class Board:

    def __init__(self, numRows, numColumns, numMines):
        self.numRows = numRows
        self.numColumns = numColumns
        self.numMines = numMines
        self.gameOver = False

        self.board = self.makeNewBoard(self.numRows, self.numColumns)

    def printState(self):
        print "This board has %(nR)x row(s), %(nC)x column(s), and %(nM)x mine(s)." % {"nR": self.numRows, "nC": self.numColumns, "nM": self.numMines}
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

    def printBoard(self):
        toPrint = ""
        for rowNum in xrange(len(self.board)):
            if rowNum == 0: 
                lineToPrint = "["
            else:
                lineToPrint = " "

            lineToPrint += str(self.board[rowNum])

            if rowNum < len(self.board) - 1: 
                lineToPrint += ", \n"
            else:
                lineToPrint += "]"

            #no real reason to individually add lineToPrint,
            #rather than directly add to toPrint, but useful
            #if we ever wanted something with individual lines
            toPrint += lineToPrint
        print toPrint



#if using imports, this would be main.py
#initialize the board
numRows = input("How many rows in the board? ")
numColumns = input("How many columns in the board? ")
numMines = input("How many mines in the board? ")

gameBoard = Board(numRows, numColumns, numMines)
gameBoard.printState()


#game loop here; keep accepting inputs until game finished
#while not gameBoard.gameOver():
#    gameBoard.step()

print "Program execution complete."

#testing ideas:
#invalid inputs for board size or mine count
#  - what if these inputs aren't numbers?
#  - what if there are too many mines (numMines > numRows * numColumns)?