from UtilityForAlgorithms import UtilityForAlgorithms

N = 4

""" This function , using forward checking, checks the attempt you're trying to perform; 
    the function will be used when the queens have been placed from
    0 to N-1 columns, because in this way we can only check the right
    side for attacking attempts """


def checkForwardAttempt(row, column, chessBoard, n):
    result = True

    # When we are at the last column, we check that each previous column has a queen positioned, so
    # the algorithm is finished and the program exits printing the chess board
    UtilityForAlgorithms.allQueensPositioned(chessBoard, column, n)

    # Variables used to remember the row and column to which we have to backtrack
    # in case we find an "illegal" column with no available cells
    backupRowForBacktracking = row
    backupColumnForBacktracking = column

    placeholder = str(row) + str(column)

    # Mark the line on the right side as unavailable
    for i in range(column + 1, n):
        if chessBoard[row][i] == '' and UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(chessBoard,
                                                                                                         row, i):
            chessBoard[row][i] = placeholder

    # Mark the right-upper diagonal as unavailable
    for index in range(1, n):
        index_row = row - index  # The lines decrease
        index_col = column + index  # The columns increase
        if UtilityForAlgorithms.checkBounds(index_row, index_col, n) and chessBoard[index_row][index_col] == '' \
                and UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(chessBoard, index_row, index_col):
            # We use x lower case because it is only temporary
            chessBoard[index_row][index_col] = placeholder

    # Mark the right-down diagonal as unavailable
    for index in range(1, n):
        index_row = row + index
        index_col = column + index
        if UtilityForAlgorithms.checkBounds(index_row, index_col, n) and chessBoard[index_row][index_col] == '' \
                and UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(chessBoard, index_row, index_col):
            # We use x lower case because it is only temporary
            chessBoard[index_row][index_col] = placeholder

    numOfFreeCells = {}

    # Iterate on the columns in order to find the number of available cells
    # for each column
    # Create a dictionary that has the columns at right as key and the number
    # of available cells on that column as value

    # Number of cells not available
    cellsNotAvailable = 0
    conditionForBacktracking = False
    while column + 1 < n:
        currentColumn = column + 1
        # Check, for each column, the rows
        for row in range(n):
            # The condition not equals to empty includes the check of 'Q' and 'F'
            if chessBoard[row][currentColumn] != '':
                cellsNotAvailable += 1

        if cellsNotAvailable == n:
            conditionForBacktracking = True

        numOfFreeCells[currentColumn] = n - cellsNotAvailable

        cellsNotAvailable = 0

        column = column + 1

    # Find the column with the least number of available cells
    numOfMinCellsAvailable = n
    freeCellsForColumnI = 0
    indexScanned = 0
    # for i in range(1, len(numOfFreeCells)):

    # if bool(numOfFreeCells):
    #     return True

    # Iterate on the columns in order to find which one has the minimum number of free cells
    for i in numOfFreeCells.keys():
        freeCellsForColumnI = numOfFreeCells[i]
        if freeCellsForColumnI != 0 and freeCellsForColumnI < numOfMinCellsAvailable:
            numOfMinCellsAvailable = freeCellsForColumnI
            indexScanned = i

    # columnToInsertValue is the column with the least number of available cells
    columnToInsertValue = indexScanned
    for i in range(n):

        if numOfMinCellsAvailable > 0 and not conditionForBacktracking:
            if chessBoard[i][
                columnToInsertValue] == '' and UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(
                chessBoard, i, columnToInsertValue):
                chessBoard[i][columnToInsertValue] = 'Q'

                # Reset the dictionary, freeCellsForColumnI, indexScanned and the chess board
                numOfFreeCells = {}
                indexScanned = 0
                freeCellsForColumnI = 0
                numOfMinCellsAvailable = n

                # Erase the temporary placeholder 'x'
                # for k in range(n):
                #     for m in range(n):
                #         if chessBoard[k][m] == 'x':
                #             chessBoard[k][m] = 'X'

                return checkForwardAttempt(i, columnToInsertValue, chessBoard, n)
        else:
            if conditionForBacktracking:  # and chessBoard[i][columnToInsertValue] != 'X' and chessBoard[i][columnToInsertValue] != 'Q':

                toContinue = True
                rowForQueenFound = 0
                while backupColumnForBacktracking >= 0 and toContinue:

                    # Search for queen in column backupColumnForBacktracking
                    for k in range(n):
                        if chessBoard[k][backupColumnForBacktracking] == 'Q':
                            rowForQueenFound = k
                            break

                    # Remove 'Q'
                    chessBoard[rowForQueenFound][backupColumnForBacktracking] = ''

                    # Rimuovi i vincoli associati ad una regina cancellata
                    for a in range(n):
                        for b in range(n):
                            if chessBoard[a][b] == str(rowForQueenFound) + str(backupColumnForBacktracking):
                                chessBoard[a][b] = ''

                    rowForQueenFound += 1
                    if rowForQueenFound == n:
                        backupColumnForBacktracking -= 1
                    else:
                        for row in range(rowForQueenFound, n):
                            if chessBoard[row][backupColumnForBacktracking] == '':
                                chessBoard[row][backupColumnForBacktracking] = 'Q'
                                toContinue = False
                                break
                            elif row == n - 1 and chessBoard[row][backupColumnForBacktracking] != '' and \
                                    chessBoard[row][backupColumnForBacktracking] != 'Q':
                                backupColumnForBacktracking -= 1

                return checkForwardAttempt(rowForQueenFound, backupColumnForBacktracking, chessBoard, n)

    return False


""" This method tries the current attempt using the same mechanism 
    of the AC-3 algorithm used by MAC: for every queen positioned,
    it detects the forbidden cells in the next right column and, 
    if no queen can be placed safely, than go back to previous 
    placed queen and put it in the next available row"""


def checkAttemptWithMAC(chessBoard, row, column, n):
    # When we are at the last column, we check that each previous column has a queen positioned, so
    # the algorithm is finished and the program prints and return the chess board
    UtilityForAlgorithms.allQueensPositioned(chessBoard, column, n)

    # Iterate on the adjacent right column, in order
    # to find the first possibility (scan at maximum
    # 3 positions)
    current_row = 0
    columnToScan = column + 1

    placeholder = str(row) + str(column)

    # Keep trace of the number of constraints in the columnToScan at this phase
    # with this counter
    numberOfConstraints = 0

    # Filling the right-up, right and right-down cell, if the cell isn't forbidden
    for index in range(row - 1, row + 2):
        if UtilityForAlgorithms.checkBounds(index, columnToScan,
                                            n) and UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(
            chessBoard, index, columnToScan):
            chessBoard[index][columnToScan] = placeholder
            numberOfConstraints += 1
            current_row = index
        elif UtilityForAlgorithms.checkBounds(index, columnToScan,
                                            n) and not UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(
            chessBoard, index, columnToScan):
            numberOfConstraints += 1

    # next_row is the row from which try to position the queen
    # If there isn't any cell in position below the last constraint, the row to scan for insert
    # queen is the first one
    next_row = current_row + 1

    # We need to iterate on the column, because we can face a not available cell
    while UtilityForAlgorithms.checkBounds(next_row, columnToScan, n) and not UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(chessBoard, next_row, columnToScan):
        next_row += 1

    if next_row > n - 1:
        next_row = 0

    # Scan the right - adjacent column from next_row to the last row to find if it's possible
    # to fill in a queen.
    # The number of cells on which to iterate is the number of total rows - the number of
    # cells containing the constraint of a positioned queen.
    # The iteration goes ahead only till a queen can't be positioned
    isPlaceable = True
    continueIteration = True
    cellOnWhichIterate = n - numberOfConstraints
    while next_row < n and cellOnWhichIterate > 0 and continueIteration:
        if chessBoard[next_row][
            columnToScan] == '' and UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(chessBoard,
                                                                                                     next_row,
                                                                                                     columnToScan):
            # When a cell is free to be inserted a queen, we check if that row already contains a queen
            for j in reversed(range(columnToScan)):
                if chessBoard[next_row][j] == 'Q':
                    isPlaceable = False
                    break
                elif j == 0:
                    isPlaceable = True
                    continueIteration = False
                    break
        if not isPlaceable:
            next_row += 1
            cellOnWhichIterate -= 1

    rowForRecursiveCall = 0
    columnForRecursiveCall = 0
    # If the column we are scanning contains a cell available to position the queen, then
    # put it in the cell and call the recursion on the indexes of that cell; otherwise,
    # we have to do a backtracking one column at a time (also scanning back all the previous columns)
    # till a column that can contain a queen is found.
    if isPlaceable:
        chessBoard[next_row][columnToScan] = 'Q'
        rowForRecursiveCall = next_row
        columnForRecursiveCall = columnToScan
    else:
        # Go back 1 column
        columnBack = columnToScan - 1

        queenToInsert = True

        while columnBack > -1 and queenToInsert:
            indexRowToInsertQueen = 0
            eraseConstraints = False
            for indexRow in range(n):
                if chessBoard[indexRow][columnBack] == 'Q':
                    chessBoard[indexRow][columnBack] = ''
                    eraseConstraints = True
                    indexRowToInsertQueen = indexRow

                # Remove the constraints related to a deleted queen
                if eraseConstraints:
                    for a in range(n):
                        for b in range(n):
                            if chessBoard[a][b] == str(indexRow) + str(columnBack):
                                chessBoard[a][b] = ''

            # When a queen is to be placed in the column of backtracking, iterate till a not blocked cell is found:
            # in a column you can have 2 or more adjacent not available cells on the same column
            indexRowToInsertQueen += 1
            while not UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(chessBoard,
                                                                                       indexRowToInsertQueen,
                                                                                       columnBack):
                indexRowToInsertQueen += 1

            # If one cell empty and satisfying the constraints is found, then put the queen
            if UtilityForAlgorithms.checkBounds(indexRowToInsertQueen, columnBack, n) and \
                    chessBoard[indexRowToInsertQueen][
                        columnBack] == '' and UtilityForAlgorithms.checkForCurrentCellFeasibleInBlockedNQueens(chessBoard, indexRowToInsertQueen, columnBack):
                chessBoard[indexRowToInsertQueen][columnBack] = 'Q'
                rowForRecursiveCall = indexRowToInsertQueen
                columnForRecursiveCall = columnBack
                queenToInsert = False

            columnBack -= 1

    return checkAttemptWithMAC(chessBoard, rowForRecursiveCall, columnForRecursiveCall, n)


def findSolutionWithBacktrackingFC(chessBoard, column, n):
    # Returns true if the queens are positioned
    if column >= n:
        UtilityForAlgorithms.printChessBoard(chessBoard, N)
        return True

    # Further checks to evaluate if the queen can be positioned
    # in other remaining possibilities
    for i in range(n):
        if checkForwardAttempt(i, column, chessBoard, n):
            # Queen is positioned
            chessBoard[i][column] = 1

        # Recursive invocation for the remaining queens
        if findSolutionWithBacktrackingFC(chessBoard, column + 1, n):
            return True

        chessBoard[i][column] = 0

    return False


def findSolutionWithBacktrackingMAC(chessBoard, column, n):
    # Returns true if the queens are positioned
    if column >= n:
        UtilityForAlgorithms.printChessBoard(chessBoard, N)
        return True

    # Further checks to evaluate if the queen can be positioned
    # in other remaining possibilities
    for i in range(1, n):
        if checkAttemptWithMAC(chessBoard, i, column, n):
            # Queen is positioned
            chessBoard[i][column] = 1
            # Recursive invocation for the remaining queens
            if findSolutionWithBacktrackingMAC(chessBoard, column + 1, n):
                return True

            chessBoard[i][column] = 0

    return False


def main():
    # First of all we use a 4x4 chess board to show that the problem is correctly solved

    # chessBoard = [['Q', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    chessBoard = [['Q', '', '', ''], ['F', 'F', '', ''], ['', '', '', ''], ['', 'F', '', '']]
    version = int(input("Press 1 for FC, 2 for MAC:"))
    if version == 1:
        result = findSolutionWithBacktrackingFC(chessBoard, 0, N)
    else:
        result = findSolutionWithBacktrackingMAC(chessBoard, 0, N)
    if not result:
        print("Error, it doesn't exist a solution")
    UtilityForAlgorithms.printChessBoard(chessBoard, N)

    # time.sleep(10)  # Wait 10 seconds before the main part of tests
    #
    #
    # values = np.arange(2, 21)
    # sumFC = []
    # sumMAC = []
    # for n in values:  # Chess board's dimensions from 2x2 to 20x20
    #     chessBoard = []
    #     sumFC = []
    #     sumMAC = []
    #
    #     for k in range(50):  # Execute 50 times for every dimension
    #         for i in range(n + 1):
    #             for j in range(n + 1):
    #                 chessBoard[i][j] = ''  # Initialize the chess board
    #
    #         chessBoard[0][0] = 'Q'
    #         start = timer()
    #         result = findSolutionWithBacktrackingFC(chessBoard, 0, n)
    #         end = timer()
    #         sumFC.append(end - start)
    #         if not result:
    #             print("It doesn't exist a solution with FC")
    #
    #     chessBoard = []
    #
    #     for k in range(50):  # Execute 50 times for every dimension
    #         for i in range(n + 1):
    #             for j in range(n + 1):
    #                 chessBoard[i][j] = ''  # Initialize the chess board
    #
    #         chessBoard[0][0] = 'Q'
    #         start = timer()
    #         result = findSolutionWithBacktrackingMAC(chessBoard, 0, n)
    #         end = timer()
    #         sumMAC.append(end - start)
    #         if not result:
    #             print("It doesn't exist a solution with MAC")
    #
    # plt.plot(values, sumFC, marker="o", color="red")
    # plt.plot(values, sumMAC, marker="o", color="green")
    # plt.show()
    return True


if __name__ == '__main__':
    main()
