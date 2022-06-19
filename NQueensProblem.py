N = 4


def checkBounds(x, y):
    return 0 < x <= N - 1 and 0 < y <= N - 1


# Function that prints the current layout of the chess board
def printChessBoard(chessBoard):
    for i in range(N):
        for j in range(N):
            print(chessBoard[i][j])
        print()


""" This function , using forward checking, checks the attempt you're trying to perform; 
    the function will be used when the queens have been placed from
    0 to N-1 columns, because in this way we can only check the left
    side for attacking attempts """


def checkForwardAttempt(row, column, chessBoard, N):
    result = True

    # Mark the line on the right side as unavailable
    for i in range(column + 1, N):
        chessBoard[row][i] = 'X'

    # Mark the right-upper diagonal as unavailable
    for index in range(1, N):
        index_row = row - index
        index_col = column + index
        if checkBounds(index_row, index_col):
            chessBoard[index_row][index_col] = 'X'

    # Mark the right-down diagonal as unavailable
    for index in range(1, N):
        index_row = row + index
        index_col = column + index
        if checkBounds(index_row, index_col):
            chessBoard[index_row][index_col] = 'X'

    numOfFreeCells = {}

    # Iterate on the columns in order to find the number of available cells
    # for each column
    # Create a dictionary that has the columns at right as key and the number
    # of available cells on that column as value
    cellsNotAvailable = 0
    while column + 1 < N:
        currentColumn = column + 1
        for row in range(N):
            if chessBoard[row][currentColumn] == 'X':
                cellsNotAvailable += 1

        numOfFreeCells[currentColumn] = N - cellsNotAvailable

        cellsNotAvailable = 0

        column = column + 1

    # Find the column with the least number of available cells
    numOfMinCellsAvailable = N
    valueScanned = 0
    indexScanned = 0
    # for i in range(1, len(numOfFreeCells)):
    for i in numOfFreeCells.keys():
        valueScanned = numOfFreeCells[i]
        if valueScanned < numOfMinCellsAvailable:
            numOfMinCellsAvailable = valueScanned
            indexScanned = i

    # columnToInsertValue is the column with the least number of available cells
    columnToInsertValue = indexScanned
    for i in range(N):

        if numOfMinCellsAvailable > 1:
            if chessBoard[i][columnToInsertValue] != 'X' and chessBoard[i][columnToInsertValue] != 'Q':
                chessBoard[i][columnToInsertValue] = 'Q'
                # Reset the dictionary, valueScanned, indexScanned and the chess board
                numOfFreeCells = {}
                indexScanned = 0
                valueScanned = 0
                numOfMinCellsAvailable = N
                return checkForwardAttempt(i, columnToInsertValue, chessBoard, N)
        else:
            if numOfMinCellsAvailable == 1 and chessBoard[i][columnToInsertValue] != 'X' and chessBoard[i][
                columnToInsertValue] != 'Q':
                chessBoard[i][columnToInsertValue] = 'Q'
                return True

    return False


""" This method tries the current attempt using the same mechanism 
    of the AC-3 algorithm used by MAC: for every queen positioned,
    it detects the forbidden cells in the next right column and, 
    if no queen can be placed safely, than go back to previous 
    placed queen and put it in the next available row"""


def checkAttemptWithAC3(chessBoard, row, column):
    # Iterate on the adjacent right column, in order
    # to find the first possibility (scan at maximum
    # 3 positions)

    current_row = 0
    columnToScan = column + 1
    # Scanning the right-up, right and right-down cell
    for index in range(row - 1, row + 2):
        if checkBounds(index, columnToScan):
            chessBoard[index][columnToScan] = 'X'
        current_row = index

    next_row = current_row + 1

    isPlaceable = True
    for i in range(1, N):
        if chessBoard[next_row][i] == 1 and i != columnToScan:
            isPlaceable = False

    rowForRecursiveCall = 0
    columnForRecursiveCall = 0
    if isPlaceable:
        chessBoard[next_row][columnToScan] = 'Q'
        rowForRecursiveCall = next_row
        columnForRecursiveCall = columnToScan
    else:
        # Scanning all the previous columns in order to check that there isn't
        # any other queen
        for index in range(1, N):
            # Go back 1 column
            columnBack = columnToScan - 1
            if chessBoard[index][columnBack] == 'Q':
                chessBoard[index][columnBack] = 0
                indexToInsertQueen = index + 1
                chessBoard[indexToInsertQueen][columnBack] = 'Q'
                rowForRecursiveCall = indexToInsertQueen
                columnForRecursiveCall = columnBack

    return checkAttemptWithAC3(chessBoard, rowForRecursiveCall, columnForRecursiveCall)


def findSolutionWithBacktracking(chessBoard, column):
    # Returns true if the queens are positioned
    if column >= N:
        # printChessBoard(chessBoard)
        return True

    # Further checks to evaluate if the queen can be positioned
    # in other remaining possibilities
    for i in range(N):
        if checkForwardAttempt(i, column, chessBoard, N):
            # Queen is positioned
            chessBoard[i][column] = 1

        """if checkAttemptWithAC3(chessBoard, i, column):
            # Queen is positioned
            chessBoard[i][column] = 1"""

        # Recursive invocation for the remaining queens
        if findSolutionWithBacktracking(chessBoard, column + 1):
            return True

        chessBoard[i][column] = 0

    return False


def main():
    chessBoard = [['Q', 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    result = findSolutionWithBacktracking(chessBoard, 0)
    if not result:
        print('It does not exist a solution')
    printChessBoard(chessBoard)
    return True


if __name__ == '__main__':
    main()
