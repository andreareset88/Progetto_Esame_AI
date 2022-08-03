from timeit import default_timer as timer
from matplotlib import pyplot as plt

N = 4


def checkBounds(x, y, n):
    return 0 <= x <= n - 1 and 0 <= y <= n - 1


# Function that prints the current layout of the chess board
def printChessBoard(chessBoard, n):
    for i in range(n):
        for j in range(n):
            if chessBoard[i][j] == '':
                print("\"\"", end=" ")
            print(chessBoard[i][j], end=" ")
        print("\n")


""" This function , using forward checking, checks the attempt you're trying to perform; 
    the function will be used when the queens have been placed from
    0 to N-1 columns, because in this way we can only check the right
    side for attacking attempts """


def checkForwardAttempt(row, column, chessBoard, n):
    result = True

    if column == n - 1:
        queenInLastColumn = False
        for i in range(n):
            if chessBoard[i][column] == 'Q':
                queenInLastColumn = True
        if queenInLastColumn:
            printChessBoard(chessBoard, n)
            exit(0)

    # Variables used to remember the row and column to which we have to backtrack 
    # in case we find an "illegal" column with no available cells
    backupRowForBacktracking = row
    backupColumnForBacktracking = column

    placeholder = str(row)+str(column)

    # Mark the line on the right side as unavailable
    for i in range(column + 1, n):
        if chessBoard[row][i] == '':
            chessBoard[row][i] = placeholder

    # Mark the right-upper diagonal as unavailable
    for index in range(1, n):
        index_row = row - index  # The lines decrease
        index_col = column + index  # The columns increase
        if checkBounds(index_row, index_col, n) and chessBoard[index_row][index_col] == '':
            # We use x lower case because it is only temporary
            chessBoard[index_row][index_col] = placeholder

    # Mark the right-down diagonal as unavailable
    for index in range(1, n):
        index_row = row + index
        index_col = column + index
        if checkBounds(index_row, index_col, n) and chessBoard[index_row][index_col] == '':
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

    # Iterate on the columns in order to find wich one has the minimum number of free cells
    for i in numOfFreeCells.keys():
        freeCellsForColumnI = numOfFreeCells[i]
        if freeCellsForColumnI != 0 and freeCellsForColumnI < numOfMinCellsAvailable:
            numOfMinCellsAvailable = freeCellsForColumnI
            indexScanned = i

    # columnToInsertValue is the column with the least number of available cells
    columnToInsertValue = indexScanned
    for i in range(n):

        if numOfMinCellsAvailable > 0 and not conditionForBacktracking:
            if chessBoard[i][columnToInsertValue] == '':
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
                            if chessBoard[a][b] == str(rowForQueenFound)+str(backupColumnForBacktracking):
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
                            elif row == n - 1 and chessBoard[row][backupColumnForBacktracking] != '' and chessBoard[row][backupColumnForBacktracking] != 'Q':
                                backupColumnForBacktracking -= 1



                # rowAfterBacktracking = backupRowForBacktracking + 1
                # # Check the previous column in order to reach the position of the queen
                #
                # indexTillLastRow = rowAfterBacktracking
                # countCellsNotAvailableOnBacktrackingColumn = 0
                # while indexTillLastRow < n:
                #     if checkBounds(indexTillLastRow, backupColumnForBacktracking, n) and chessBoard[indexTillLastRow][backupColumnForBacktracking] == '':
                #         chessBoard[indexTillLastRow][backupColumnForBacktracking] = 'Q'
                #         break
                #     elif indexTillLastRow == n-1 and chessBoard[indexTillLastRow][backupColumnForBacktracking] != '' and chessBoard[indexTillLastRow][backupColumnForBacktracking] != 'Q':
                #         backupColumnForBacktracking -= 1
                #
                #         for k in range(n):
                #             if chessBoard[k][backupColumnForBacktracking] == 'Q':
                #                 rowAfterBacktracking = k
                #
                #                 chessBoard[k][backupColumnForBacktracking] = ''
                #
                #                 # Rimuovi i vincoli associati ad una regina cancellata
                #                 for a in range(n):
                #                     for b in range(n):
                #                         if chessBoard[a][b] == str(k) + str(backupColumnForBacktracking):
                #                             chessBoard[a][b] = ''
                #
                #     # elif checkBounds(indexTillLastRow, backupColumnForBacktracking, n) and chessBoard[indexTillLastRow][backupColumnForBacktracking] != '':
                #         # countCellsNotAvailableOnBacktrackingColumn += 1
                #
                #     indexTillLastRow += 1
                #
                # # If in the current column you can't place any queen, step 1 column back
                # if countCellsNotAvailableOnBacktrackingColumn == n - backupRowForBacktracking - 1:
                #     # backupColumnForBacktracking -= 1
                #     # k è l'indice della riga dove si trova la regina (nella colonna precedente)
                #     # for k in range(n):
                #     #     if chessBoard[k][backupColumnForBacktracking] == 'Q':
                #     #         rowAfterBacktracking = k
                #     #
                #     #         chessBoard[k][backupColumnForBacktracking] = ''
                #     #
                #     #         # Rimuovi i vincoli associati ad una regina cancellata
                #     #         for a in range(n):
                #     #             for b in range(n):
                #     #                 if chessBoard[a][b] == str(k)+str(backupColumnForBacktracking):
                #     #                     chessBoard[a][b] = ''

                return checkForwardAttempt(rowForQueenFound, backupColumnForBacktracking, chessBoard, n)

    return False


""" This method tries the current attempt using the same mechanism 
    of the AC-3 algorithm used by MAC: for every queen positioned,
    it detects the forbidden cells in the next right column and, 
    if no queen can be placed safely, than go back to previous 
    placed queen and put it in the next available row"""


def checkAttemptWithMAC(chessBoard, row, column, n):
    # Iterate on the adjacent right column, in order
    # to find the first possibility (scan at maximum
    # 3 positions)

    current_row = 0
    columnToScan = column + 1
    # Scanning the right-up, right and right-down cell
    for index in range(row - 1, row + 2):
        if checkBounds(index, columnToScan, n):
            chessBoard[index][columnToScan] = 'X'
        current_row = index

    next_row = current_row + 1

    isPlaceable = True
    for i in range(1, n):
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
        for index in range(1, n):
            # Go back 1 column
            columnBack = columnToScan - 1
            if chessBoard[index][columnBack] == 'Q':
                chessBoard[index][columnBack] = 0
                indexToInsertQueen = index + 1
                chessBoard[indexToInsertQueen][columnBack] = 'Q'
                rowForRecursiveCall = indexToInsertQueen
                columnForRecursiveCall = columnBack

    return checkAttemptWithMAC(chessBoard, rowForRecursiveCall, columnForRecursiveCall, n)


def findSolutionWithBacktrackingFC(chessBoard, column, n):
    # Returns true if the queens are positioned
    if column >= n:
        # printChessBoard(chessBoard)
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
        # printChessBoard(chessBoard)
        return True

    # Further checks to evaluate if the queen can be positioned
    # in other remaining possibilities
    for i in range(n):
        if checkAttemptWithMAC(chessBoard, i, column, n):
            # Queen is positioned
            chessBoard[i][column] = 1
            # Recursive invocation for the remaining queens
            if findSolutionWithBacktrackingMAC(chessBoard, column + 1, n):
                return True

            chessBoard[i][column] = 0

    return False


def main():
    chessBoard = [['Q', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    version = int(input("Press 1 for FC, 2 for MAC:"))
    if version == 1:
        result = findSolutionWithBacktrackingFC(chessBoard, 0, N)
    else:
        result = findSolutionWithBacktrackingMAC(chessBoard, 0, N)
    if not result:
        print("Error, it doesn't exist a solution")
    printChessBoard(chessBoard, N)

    """for n in range(2, 21):  # Dimensione scacchiera crescente da 2x2 a 20x20
        chessBoard = []
        sumFC = []
        sumMAC = []

        # for k in range(50):  # Eseguo 50 volte per ogni dimensione
            for i in range(n+1):
                for j in range(n+1):
                    chessBoard[i][j] = 0

            chessBoard[0][0] = 'Q'
            start = timer()
            result = findSolutionWithBacktrackingFC(chessBoard, 0, n)
            end = timer()
            sumFC.append(end - start)
            if not result:
                print('It does not exist a solution with FC')
            # printChessBoard(chessBoard, n)
        
        chessBoard = []
        # for k in range(50):
            for i in range(n):
                for j in range(n):
                    chessBoard[i][j] = 0

            chessBoard[0][0] = 'Q'
            start = timer()
            result = findSolutionWithBacktrackingMAC(chessBoard, 0, n)
            end = timer()
            sumMAC.append(end - start)
            if not result:
                print('It does not exist a solution with MAC')
            # printChessBoard(chessBoard, n)
        plt.plot(n, sumFC, marker="o", color="red")
        plt.plot(n, sumMAC, marker="o", color="green")
    plt.show()"""
    return True


if __name__ == '__main__':
    main()
