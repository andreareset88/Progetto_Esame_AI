# This method prints the chess board to check the current state.
def printChessBoard(chessBoard):
    for i in range(4):
        for j in range(4):
            print(chessBoard[i][j])
        print()


 """ This function checks the attempt you're trying to perform; 
 the function will be used when the queens have been placed from
 0 to N-1 columns, because in this way we can only check the left
 side for attacking attempts """
def checkAttempt(row, column, chessBoard):
    for i in range(column):
        if chessBoard[row][i] == 1:
            return False

    for i, j in zip(range(row, 4, 1), range(column, -1, -1)):
        if chessBoard[i][j] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(column, -1, -1)):
        if chessBoard[i][j] == 1:
            return False

    return True

def findSolutionWithBacktracking(chessBoard, column):
    # Returns true if the queens are positioned
    if column >= 4:
        printChessBoard(chessBoard)
        return True

    # Further checks to evaluate if the queen can be positioned
    # in other remaining possibilities
    for i in range(4):
