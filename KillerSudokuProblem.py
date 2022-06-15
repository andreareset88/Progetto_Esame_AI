import json
import sys

def printSudokuGrid(sudokuGrid):
    for i in range(0, 9):
        for j in range(0, 9):
            print(sudokuGrid[i][j])
        print("\n")


def defineCagesFromJson(json):
    for cage in json:
        cage['cells'] = [tuple(cell) for cell in cage['cells']]
    return json

def initializeSudokuGrid():
    sudokuGrid = [[0 for i in range(0, 9)] for i in range(0, 9)]
    return sudokuGrid

# Checks that each cage doesn't contain duplicated values
def checkCagesNotContainingDuplicateValues(cages):
    cells = [cell for cage in cages for cell in cage['cells']]
    if len(set(cells)) != len(cells):
        raise ValueError('Not valid json, please remove double coordinates before moving forward')

# Add the totalValue values to the 0 grid
def addTotalValueToEachCage(cages):
    sudokuGrid = [[0 for i in range(0, 9)] for i in range(0, 9)]
    for cage in cages:
        for i, j in cage['cells']:
            sudokuGrid[i][j] = cage['totalValue']

    printSudokuGrid(sudokuGrid)

# Checks that there aren't duplicated values in each column
def checkDuplicatedValuesInColumns(sudokuGrid, value, j):
    for i in range(0, 9):
        if sudokuGrid[i][j] == value:
            return False

# Checks that there aren't duplicated values in each row
def checkDuplicatedValuesInRows(sudokuGrid, value, i):
    for j in range(0, 9):
        if sudokuGrid[i][j] == value:
            return False

# Checks that there aren't duplicated values in each sub-square 3x3
def checkDuplicatedValuesInSquares(sudokuGrid, value, i, j):
    i_1 = (i//3) * 3
    j_1 = (j//3) * 3
    for row in range(0, 3):
        for column in range(0, 3):
            if sudokuGrid[i_1 + row][j_1 + column] == value:
                return False

# Checks that all the cells in each cage doesn't contain 0 elements
def checkBoxesNotContainingZero(cageElements):
    return 0 not in cageElements


def inferenceOnPossibleAssignmentsWithFC(i, j, value, sudokuGrid, setOfCells):

    checkDuplicatedValuesInSquares(sudokuGrid, value, i, j)
    checkDuplicatedValuesInRows(sudokuGrid, value, i)
    checkDuplicatedValuesInColumns(sudokuGrid, value, j)

    currentCage = setOfCells[(i, j)]

    # Cage elements is a list containing the real values
    # initialized with the empty list
    cage_elements = list()

    for row_cell, column_cell in currentCage['cells']:
        if row_cell == i and column_cell == j:
            cage_elements.append(value)
        else:
            cage_elements.append(sudokuGrid[row_cell][column_cell])

    sumToCheck = sum(cage_elements)
    if sumToCheck > currentCage['totalValue']:
        return False

    if checkBoxesNotContainingZero(cage_elements):
        if currentCage['totalValue'] != sumToCheck:
            return False

        if len(set(cage_elements)) != len(cage_elements):
            return False

    return True

def check(i, j):
    return i > 0 and j > 0


def inferenceOnPossibleAssignmentsWithMAC(i, j, value, sudokuGrid, setOfCells):

    currentCage = setOfCells[(i, j)]


    # Scan all the cells of each cage, starting from the column at the leftmost position
    # and find the couple of indexes that represents the indexes of the leftmost cell
    # of the cage
    minColumnIndexForCellsInCages = 1
    minRowIndexForCellsInCages = 1
    for row, column in currentCage['cells']:
        if column <= minColumnIndexForCellsInCages and row <= minRowIndexForCellsInCages:
            minRowIndexForCellsInCages = row
            minColumnIndexForCellsInCages = column

    cageAdjacentCells = list()

    # Scan all the elements of the cage, in order to find the adjacent ones
    for row, column in currentCage['cells']:

        # Scanning the elements on the same cage, checking the above and below row,
        # and the adjacent column
        if sudokuGrid[row][column] != 0 and row == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages + 1:
            cageAdjacentCells.append([row, column])
        if sudokuGrid[row][column] != 0 and row - 1 == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages:
            cageAdjacentCells.append([row, column])
        if sudokuGrid[row][column] != 0 and row + 1 == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages:
            cageAdjacentCells.append([row, column])


    # Before insert the value, check that it satisfies the constraints
    # existing on the grid

    # Collect adjacent cells without value

    adjacentCellsWithoutValue = list()
    for row, column in cageAdjacentCells:
        if sudokuGrid[row][column] == 0:
            adjacentCellsWithoutValue.append([row, column])

    # Iterate on all the adjacent cells and verify if the value can be assigned
    # to one of these cells, otherwise re-iterate on those cells
    for row, column in adjacentCellsWithoutValue:

        isDuplicatedValuesInSquare = checkDuplicatedValuesInSquares(sudokuGrid, value, i, j)
        isDuplicatedValuesInRow = checkDuplicatedValuesInRows(sudokuGrid, value, i)
        isDuplicatedValuesInColumn = checkDuplicatedValuesInColumns(sudokuGrid, value, j)

        if isDuplicatedValuesInSquare and isDuplicatedValuesInRow and isDuplicatedValuesInColumn:
            sudokuGrid[row][column] = value
        else:
            inferenceOnPossibleAssignmentsWithMAC(row, column, value, sudokuGrid, setOfCells)




def callBacktrack(setOfCells):
    global sudokuGrid
    for i in range(9):
        for j in range(9):
            if sudokuGrid[i][j] == 0:
                for value in range(1, 10):
                    if inferenceOnPossibleAssignmentsWithFC(i, j, value, sudokuGrid, setOfCells):
                        sudokuGrid[i][j] = value
                        callBacktrack(setOfCells)
                        sudokuGrid[i][j] = 0
                return
        printSudokuGrid(sudokuGrid)

def sudokuSolver():

# Second argument from command line
dataSourceFile = sys.argv[1]
cages = json.load(open(dataSourceFile))

cages = defineCagesFromJson(cages)

checkCagesNotContainingDuplicateValues(cages)

addTotalValueToEachCage(cages)

sudokuGrid = initializeSudokuGrid()

# All the cells of all cages
setOfCells = {cell: cage for cage in cages for cell in cage['cells']}

callBacktrack()