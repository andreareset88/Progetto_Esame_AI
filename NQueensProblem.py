from timeit import default_timer as timer
from matplotlib import pyplot as plt
import time
import numpy as np

from UtilityForAlgorithms import UtilityForAlgorithms

N = 4
operationFC = 0
operationMAC = 0

""" This function, using forward checking, checks the attempt you're trying to perform; 
    the function will be used when the queens have been placed from
    0 to N-1 columns, because in this way we can only check the right
    side for attacking attempts """


def checkAttemptWithFC(row, column, chessBoard, n, operations):
    # When we are at the last column, we check that each previous column has a queen positioned, so
    # the algorithm is finished and the program exits printing the chess board
    if UtilityForAlgorithms.allQueensPositioned(chessBoard, column, n):
        # print("Number of operations with Forward Checking: " + str(operations))
        return True, operations

    # Variables used to remember the row and column to which we have to backtrack 
    # in case we find an "illegal" column with no available cells
    backupRowForBacktracking = row
    backupColumnForBacktracking = column

    placeholder = str(row) + str(column)

    # Mark the line on the right side as unavailable
    for i in range(column + 1, n):
        if UtilityForAlgorithms.checkBounds(row, i, n) and chessBoard[row][i] == '':
            chessBoard[row][i] = placeholder
            operations += 1

    # Mark the right-upper diagonal as unavailable
    for index in range(1, n):
        index_row = row - index  # The lines decrease
        index_col = column + index  # The columns increase
        if UtilityForAlgorithms.checkBounds(index_row, index_col, n) and chessBoard[index_row][index_col] == '':
            # We use x lower case because it is only temporary
            chessBoard[index_row][index_col] = placeholder
            operations += 1

    # Mark the right-down diagonal as unavailable
    for index in range(1, n):
        index_row = row + index
        index_col = column + index
        if UtilityForAlgorithms.checkBounds(index_row, index_col, n) and chessBoard[index_row][index_col] == '':
            # We use x lower case because it is only temporary
            chessBoard[index_row][index_col] = placeholder
            operations += 1

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
            if chessBoard[row][currentColumn] != '':
                cellsNotAvailable += 1


        numOfFreeCells[currentColumn] = n - cellsNotAvailable

        if cellsNotAvailable == n:
            conditionForBacktracking = True
        elif numOfFreeCells[currentColumn] >= 1:
            column += 1
            break

        cellsNotAvailable = 0

        column = column + 1

    # Find the column with the least number of available cells
    numOfMinCellsAvailable = n
    freeCellsForColumnI = 0
    indexScanned = column

    # Iterate on the columns in order to find which one has the minimum number of free cells
    for i in numOfFreeCells.keys():
        freeCellsForColumnI = numOfFreeCells[i]
        if freeCellsForColumnI == 0:
            indexScanned = i
            break
        if freeCellsForColumnI != 0 and freeCellsForColumnI < numOfMinCellsAvailable:
            numOfMinCellsAvailable = freeCellsForColumnI
            indexScanned = i

    # columnToInsertValue is the column with the least number of available cells
    columnToInsertValue = indexScanned
    for i in range(n):

        if numOfMinCellsAvailable > 0 and not conditionForBacktracking:
            if chessBoard[i][columnToInsertValue] == '':
                chessBoard[i][columnToInsertValue] = 'Q'
                operations += 1

                # Reset the dictionary, freeCellsForColumnI, indexScanned and the chess board
                numOfFreeCells = {}
                indexScanned = 0
                freeCellsForColumnI = 0
                numOfMinCellsAvailable = n

                return checkAttemptWithFC(i, columnToInsertValue, chessBoard, n, operations)
        else:
            if conditionForBacktracking:

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
                    operations += 1

                    # Remove the constraints associated to a deleted queen
                    for a in range(n):
                        for b in range(n):
                            if chessBoard[a][b] == str(rowForQueenFound) + str(backupColumnForBacktracking):
                                chessBoard[a][b] = ''
                                operations += 1

                    rowForQueenFound += 1
                    while rowForQueenFound <= n - 1 and chessBoard[rowForQueenFound][backupColumnForBacktracking] != '':
                        rowForQueenFound += 1
                    if rowForQueenFound == n:
                        backupColumnForBacktracking -= 1
                    else:
                        for row in range(rowForQueenFound, n):
                            if chessBoard[row][backupColumnForBacktracking] == '':
                                chessBoard[row][backupColumnForBacktracking] = 'Q'
                                operations += 1
                                toContinue = False
                                break
                            elif row == n - 1 and chessBoard[row][backupColumnForBacktracking] != '' and \
                                    chessBoard[row][backupColumnForBacktracking] != 'Q':
                                backupColumnForBacktracking -= 1

                return checkAttemptWithFC(rowForQueenFound, backupColumnForBacktracking, chessBoard, n, operations)

    return False


""" This method tries the current attempt using the same mechanism 
    of the AC-3 algorithm used by MAC: for every queen positioned,
    it detects the forbidden cells in the next right column and, 
    if no queen can be placed safely, than go back to previous 
    placed queen and put it in the next available row"""


def checkAttemptWithMAC(chessBoard, row, column, n, operations):
    # When we are at the last column, we check that each previous column has a queen positioned, so
    # the algorithm is finished and the program prints and return the chess board
    if UtilityForAlgorithms.allQueensPositioned(chessBoard, column, n):
        # print("Number of operations with MAC: " + str(operations))
        return True, operations

    # Iterate on the adjacent right column, in order
    # to find the first possibility (scan at maximum
    # 3 positions)
    current_row = 0
    columnToScan = column + 1

    placeholder = str(row) + str(column)

    # Keep trace of the number of constraints in the columnToScan at this phase
    # with this counter
    numberOfConstraints = 0

    # Filling the right-up, right and right-down cell
    for index in range(row - 1, row + 2):
        if UtilityForAlgorithms.checkBounds(index, columnToScan, n):
            chessBoard[index][columnToScan] = placeholder
            operations += 1
            numberOfConstraints += 1
            current_row = index

    # next_row is the row from which try to position the queen
    # If there isn't any cell in position below the last constraint, the row to scan for insert
    # queen is the first one
    next_row = current_row + 1
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
        if chessBoard[next_row][columnToScan] == '':
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
        operations += 1
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
                    operations += 1
                    eraseConstraints = True
                    indexRowToInsertQueen = indexRow

                # Remove the constraints related to a deleted queen
                if eraseConstraints:
                    for a in range(n):
                        for b in range(n):
                            if chessBoard[a][b] == str(indexRow) + str(columnBack):
                                chessBoard[a][b] = ''
                                operations += 1

            indexRowToInsertQueen += 1

            # If one cell empty and satisfying the constraints is found, then put the queen
            if UtilityForAlgorithms.checkBounds(indexRowToInsertQueen, columnBack, n) and \
                    chessBoard[indexRowToInsertQueen][columnBack] == '':
                chessBoard[indexRowToInsertQueen][columnBack] = 'Q'
                operations += 1
                rowForRecursiveCall = indexRowToInsertQueen
                columnForRecursiveCall = columnBack
                queenToInsert = False

            columnBack -= 1

    return checkAttemptWithMAC(chessBoard, rowForRecursiveCall, columnForRecursiveCall, n, operations)


def main():
    # First of all we use a 4x4 chess board to show that the problem is correctly solved

    chessBoard = [['Q', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    version = int(input("Press 1 for FC, 2 for MAC:"))
    if version == 1:
        print("Solution found with Forward Checking:")
        print("\n")
        result = checkAttemptWithFC(0, 0, chessBoard, N, operationFC)
    else:
        print("Solution found with MAC:")
        print("\n")
        result = checkAttemptWithMAC(chessBoard, 0, 0, N, operationMAC)
    print("\n")
    if not result:
        print("Error, it doesn't exist a solution")

    print("Waiting 10 seconds before the beginning of main tests...")


    time.sleep(10)  # Wait 10 seconds before the main part of tests

    # ------------------------------------- MAIN TESTS ------------------------------------

    values = np.arange(4, 14, 1)  # chessboard dimensions from 4x4 to 13x13

    # Counters for updating the number of total operations for each chessboard's dimension
    totalOperationsWithFC = 0
    totalOperationsWithMAC = 0

    # Counters for updating the number of total operations
    numOpMac = 0
    numOpFc = 0

    # Arrays for storing total operations made
    numberOfOperationsWithFC = []
    numberOfOperationsWithMAC = []

    # Counters for updating the total execution time
    totalTimeFC = 0
    totalTimeMAC = 0

    # Arrays for storing total execution times
    sumFC = []
    sumMAC = []

    # Number of iterations for every dimension
    numIterations = 50

    # Chessboard's dimensions defined by values (nxn)
    for n in values:
        totalTime = 0

        # Execute numIterations times for every dimension
        for k in range(numIterations):

            # Initialize the nxn chessboard with all empty spaces ('')
            chessBoard = [['' for i in range(n)] for j in range(n)]

            # By default, we put the first 'Q' in the position [0,0]
            chessBoard[0][0] = 'Q'
            start = timer()
            result, numOperationsWithFC = checkAttemptWithFC(0, 0, chessBoard, n, operationFC)
            end = timer()
            totalTime += end - start
            totalOperationsWithFC += numOperationsWithFC
            if not result:
                print("It doesn't exist a solution with FC")

        totalTimeFC += totalTime
        numOpFc += totalOperationsWithFC
        sumFC.append(totalTime)
        numberOfOperationsWithFC.append(totalOperationsWithFC)
        totalTime = 0


        # Execute numIterations times for every dimension
        for k in range(numIterations):

            # Initialize the nxn chessboard with empty spaces ('')
            chessBoard = [['' for i in range(n)] for j in range(n)]

            # By default, we put the first 'Q' in the position [0,0]
            chessBoard[0][0] = 'Q'
            start = timer()
            result, numOperationsWithMAC = checkAttemptWithMAC(chessBoard, 0, 0, n, operationMAC)
            end = timer()
            totalOperationsWithMAC += numOperationsWithMAC
            totalTime += end - start
            if not result:
                print("It doesn't exist a solution with MAC")

        totalTimeMAC += totalTime
        numOpMac += totalOperationsWithMAC
        sumMAC.append(totalTime)
        numberOfOperationsWithMAC.append(totalOperationsWithMAC)

    print("TOTAL OPERATIONS (including placing a 'Q' and its constraints, "
          "but also removing them) ")
    print("\n")
    print("Total operations made by Forward Checking: " + str(numOpFc))
    print("Total operations made by MAC: " + str(numOpMac))
    print("\n")
    print("TOTAL EXECUTION TIMES")
    print("\n")
    print("Total execution time with Forward Checking: " + str(totalTimeFC) + " seconds")
    print("Total execution time with MAC: " + str(totalTimeMAC) + " seconds")
    plt.plot(values, sumFC)
    plt.plot(values, sumMAC)
    plt.xlabel("Values")
    plt.ylabel("Execution times")
    plt.legend(['Forward Checking', 'MAC'])
    plt.savefig("TimesNQueens.png")
    plt.show()
    plt.plot(values, numberOfOperationsWithFC)
    plt.plot(values, numberOfOperationsWithMAC)
    plt.xlabel("Values")
    plt.ylabel("Number of operations")
    plt.legend(['Forward Checking', 'MAC'])
    plt.savefig("OperationsNQueens.png")
    plt.show()

    # totalTime = 0
    # chessBoard = [['' for i in range(7)] for j in range(7)]
    # # for i in range(n):
    # #     for j in range(n):
    # #         chessBoard[i][j] = ''  # Initialize the chess board
    #
    # chessBoard[0][0] = 'Q'
    # start = timer()
    # result, numOperationsWithMAC = checkAttemptWithMAC(chessBoard, 0, 0, 7, operationMAC)
    # end = timer()
    # totalTime += end - start
    # totalOperationsWithMAC += numOperationsWithMAC
    # # chessBoard = []
    # print("Time MAC: " + str(totalTime) + ", operations: " + str(totalOperationsWithMAC))
    # if not result:
    #     print("It doesn't exist a solution with MAC")

    return True


if __name__ == '__main__':
    main()
