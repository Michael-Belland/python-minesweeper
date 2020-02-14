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
#The bottom-left is (0,0), the space to the right is (1,0), and so on.
#
#in retrospect, using X/Y for player coordinates and internal coordinates
#in this class was not a good idea.  It creates significant confusion over
#which coordinate system is being used and when to convert coordinates.
class Board:

    def __init__(self, numRows, numColumns, numMines):
        self.numRows = numRows
        self.numColumns = numColumns
        self.numMines = numMines
        self.mines = set()
        self.numFlags = 0
        self.gameOver = False

        #Honestly, an object oriented approach (a 2d array of Cells, with subclassing)
        #would probably be more intuitive than this design.  But let's see where this goes.
        self.stateBoard = self.makeNewBoard(self.numRows, self.numColumns)
        self.playerBoard = self.makeNewBoard(self.numRows, self.numColumns, "#")
        self.isBoardSet = False

    def printState(self, printHidden = False):
        numLeft = self.numMines - self.numFlags
        print "This board has %(nR)d row(s), %(nC)d column(s), and %(nM)d mine(s)." % {"nR": self.numRows, "nC": self.numColumns, "nM": self.numMines}
        print "This board has %(nF)d flag(s). Look out for %(nL)d mine(s)!" % {"nF": self.numFlags, "nL": numLeft}
        if printHidden:
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

        if self.numRows*self.numColumns < self.numMines+len(ignoredSpaceList):
            self.isBoardSet = False
            print "Error: too many mines to fit in board."
            return

        while len(self.mines) < self.numMines:
            i = randint(0, self.numColumns-1)
            j = randint(0, self.numRows-1)
            if (i,j) not in self.mines and (i,j) not in ignoredSpaceList:
                self.mines.add((i,j))
                self.stateBoard[j][i] = "M"

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

        self.isBoardSet = True

    #a player should only be able to flag a non-revealed square
    #a flagged square should not be revealed, even by other squares
    def playerToggleFlag(self, flagX, flagY):
        if self.playerBoard[-flagY-1][flagX] == "#":
            self.playerBoard[-flagY-1][flagX] = "F"
            self.numFlags += 1
        elif self.playerBoard[-flagY-1][flagX] == "F":
            self.playerBoard[-flagY-1][flagX] = "#"
            self.numFlags -= 1
        else:
            print "You can't put a flag on a cleared space!"

    def playerProbeSquare(self, probeX, probeY):
        boardX = probeX
        boardY = self.numRows-probeY-1

        if self.playerBoard[boardY][boardX] == "F":
            print "To uncover this space, remove the flag at (%(probeX)d, %(probeY)d) first." % {"probeX": probeX, "probeY": probeY}
            return
        elif self.playerBoard[boardY][boardX] != "#":
            print "You can't clear an already cleared space!"
            return

        #Don't populate mines until after user's first valid probe.
        if self.isBoardSet == False:
            self.populateMines([(boardX, boardY)])

        self.playerBoard[boardY][boardX] = self.stateBoard[boardY][boardX]

        if self.stateBoard[boardY][boardX] == "M":
            print "You uncovered a mine!  Game over."
            self.gameOver = True

        elif self.stateBoard[boardY][boardX] == 0:

            for neighbor in self.getNeighborSet(boardX, boardY):
                neighborX = neighbor[0]
                neighborY = neighbor[1]

                #only propagate to covered, non-flagged squares
                if self.playerBoard[neighborY][neighborX] == "#":
                    self.propagateProbeSquare(neighborX, neighborY)

        #no special action for other squares

    #propagation of clearing a board to neighbors of an uncovered 0
    #this function accepts internal board coordinates, and provides a way to separate
    #player-performed actions from computer-performed actions (for example, for counting
    #number of user inputs used to finish a game)
    def propagateProbeSquare(self, boardX, boardY):
        assert self.isBoardSet

        assert self.playerBoard[boardY][boardX] == "#"

        assert self.stateBoard[boardY][boardX] != "M"

        if self.stateBoard[boardY][boardX] == 0:

            self.playerBoard[boardY][boardX] = self.stateBoard[boardY][boardX]

            for neighbor in self.getNeighborSet(boardX, boardY):
                neighborX = neighbor[0]
                neighborY = neighbor[1]
                if self.playerBoard[neighborY][neighborX] == "#":
                    self.propagateProbeSquare(neighborX, neighborY)

        else:
            #change the player board to reflect the number on the hidden board,
            #then stop propagation, as at least one neighbor is a mine
            self.playerBoard[boardY][boardX] = self.stateBoard[boardY][boardX]

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

    def isBoardFinished(self):
        if self.gameOver:
            gameBoard.printState(True)
            return True
        for rowNum in xrange(self.numRows):
            for columnNum in xrange(self.numColumns):
                if self.stateBoard[rowNum][columnNum] != "M":
                    if self.playerBoard[rowNum][columnNum] == "#" or self.playerBoard[rowNum][columnNum] == "F":
                        return False
        print "You Win!"
        gameBoard.printState(True)
        return True

def main():
    doReplayGame = True
    argumentMismatchErrorMsg = "Error: Incorrect number of arguments.  For how to use commands, enter \"help\".  To end the game, enter \"quit\"."

    while(doReplayGame):
        #initialize the board
        numRows = int(raw_input("How many rows in the board? "))
        numColumns = int(raw_input("How many columns in the board? "))
        numMines = int(raw_input("How many mines in the board? "))

        gameBoard = Board(numRows, numColumns, numMines)
        gameBoard.printState(False) #set to True to cheat and see the hidden board

        boardActions = ["probe", "flag", "quit", "new", "help"]
        quitFlag = False

        print "Board actions: "+prettyPrintBasicList(boardActions)
        print "Coordinate system: bottom-left is 0,0.  To the right, the first number increases; as you move up, the second number increases."

        while gameBoard.isBoardFinished() is False:

            gameBoard.printState(False) #set to True to cheat and see the hidden board

            userInput = raw_input("Enter board action: ").split()
            if len(userInput) == 0:
                print "ERROR: No user input detected.  For how to use commands, enter \"help\".  To end the game, enter \"quit\"."
                continue
            userAction = userInput[0]

            if userAction == "probe":
                if len(userInput) != 3:
                    print argumentMismatchErrorMsg
                    continue
                userX = int(userInput[1])
                userY = int(userInput[2])
                gameBoard.playerProbeSquare(userX, userY)

            elif userAction == "flag":
                if len(userInput) != 3:
                    print argumentMismatchErrorMsg
                    continue
                userX = int(userInput[1])
                userY = int(userInput[2])
                gameBoard.playerToggleFlag(userX, userY)

            elif userAction == "quit":
                #Could check argument list length, but if you type "quit" first, you probably just want to quit.
                quitFlag = True
                doReplayGame = False
                break

            elif userAction == "new":
                #Same as above with "quit".  If you write "new", anything after it is ignored.
                quitFlag = True
                doReplayGame = True
                break

            elif userAction == "help":
                #Same as above with "quit".  If you write "help", anything after it is ignored, and help for all commands appears.
                print "To uncover a space, enter \"probe\" followed by coordinates. (e.g. probe 0 1)"
                print "To flag a space, or to remove a flag from a space with one, enter \"flag\" followed by coordinates. (e.g. flag 0 1)"
                print "To quit the game, enter \"quit\"."
                print "To abandon the current game and start a new one, enter \"new\"."
                print "To see these instructions, enter \"help\"."
                pauseInput = raw_input("Press the Enter key to continue... ")

            else:
                print "Error: did not recognize user action \""+userAction+"\""

        if quitFlag:
            continue

        replayGameResponse = raw_input("Would you like to play another game? (y for yes, any other input for no.) ")
        if replayGameResponse != "y":
            doReplayGame = False

    print "Program execution complete."

if __name__ == "__main__":
    main()

#testing ideas:
#invalid inputs for board size or mine count
#  - what if these inputs aren't numbers?
#  - what if there are too many mines (numMines > numRows * numColumns)?
#  - what if the user probes a square at an x-coordinate i where 0 <= i < numColumns isn't True?