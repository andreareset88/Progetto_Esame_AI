class UtilityForAlgorithms:

    # Function that prints the current layout of the chess board
    @staticmethod
    def printChessBoard(chessBoard, n):
        for i in range(n):
            for j in range(n):
                if chessBoard[i][j] == '':
                    print("\"\"", end=" ")
                print(chessBoard[i][j], end=" ")
            print("\n")
        print("-----------------")
        print("\n")

    # Function that checks the bounds of the indexes of the chess board
    @staticmethod
    def checkBounds(x, y, n):
        return 0 <= x <= n - 1 and 0 <= y <= n - 1

    # Function that initializes the chess board for the blocked n queens problem with some cells
    # marked as forbidden ('F')
    @staticmethod
    def initializeGridExcludingSpecifiedValuesInBlockedNQueens(chessBoard, notAllowedValues):
        for row, column in notAllowedValues:
            chessBoard[row][column] = 'F'

    # Checks if the cell is available or not allowed
    @staticmethod
    def isAFreeCell(chessBoard, row, column):
        result = True
        if chessBoard[row][column] == 'F':
            result = False

        return result

    # Function that checks if there's a queen positioned in the last column of the chess board;
    # if there is, the solution has been found and the chess board is printed
    @staticmethod
    def allQueensPositioned(chessBoard, column, n):
        result = False
        if column == n - 1:
            queenInLastColumn = False
            for i in range(n):
                if chessBoard[i][column] == 'Q':
                    queenInLastColumn = True
                    result = True
                    break
            if queenInLastColumn:
                UtilityForAlgorithms.printChessBoard(chessBoard, n)

        return result

    # Function that prints the sudoku grid
    @staticmethod
    def printSudokuGrid(sudokuGrid):
        for i in range(9):
            for j in range(9):
                print(sudokuGrid[i][j], end="|")
            print("\n")

    # Initialize the sudoku grid with all 0
    @staticmethod
    def initializeSudokuGrid():
        sudokuGrid = [[0 for i in range(0, 9)] for i in range(0, 9)]
        return sudokuGrid
