class Board:

    def __init__(self, numRows, numColumns, numMines):
        self.numRows = numRows
        self.numColumns = numColumns
        self.numMines = numMines

    def printState(self):
        print "This board has %(nR)x rows, %(nC)x columns, and %(nM)x mines." % {"nR": self.numRows, "nC": self.numColumns, "nM": self.numMines}

#initialize the board
numRows = input("How many rows in the board? ")
numColumns = input("How many columns in the board? ")
numMines = input("How many mines in the board? ")

gameBoard = Board(numRows, numColumns, numMines)
gameBoard.printState()