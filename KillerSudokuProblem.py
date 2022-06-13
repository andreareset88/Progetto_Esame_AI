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

def checkCagesNotContainingDuplicateValues(cages):
    cells = [cell for cage in cages for cell in cage['cells']]
    if len(set(cells)) != len(cells):
        raise ValueError('Not valid json, please remove double coordinates before moving forward')


def addTotalValueToEachCage(cages):
    sudokuGrid = [[0 for i in range(0, 9)] for i in range(0, 9)]
    for cage in cages:
        for i, j in cage['cells']:
            sudokuGrid[i][j] = cage['totalValue']

    printSudokuGrid(sudokuGrid)

def checkDoubleValuesInColumns(sudokuGrid, value, j):
    for i in range(0, 9):
        if sudokuGrid[i][j] == value:
            return False

def checkDoubleValuesInRows(sudokuGrid, value, i):
    for j in range(0, 9):
        if sudokuGrid[i][j] == value:
            return False

def checkDoubleValuesInSquares(sudokuGrid, value, i, j):
    i_1 = (i//3) * 3
    j_1 = (j//3) * 3
    for row in range(0, 3):
        for column in range(0, 3):
            if sudokuGrid[i_1 + row][j_1 + column] == value:
                return False


def inferenceOnAvailablePossibleAssignments(i, j, value, sudokuGrid, setOfCells):

    checkDoubleValuesInSquares(sudokuGrid, value, i, j)
    checkDoubleValuesInRows(sudokuGrid, value, i)
    checkDoubleValuesInColumns(sudokuGrid, value, j)

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




def callBacktrack(setOfCells):
    global sudokuGrid
    for i in range(9):
        for j in range(9):
            if sudokuGrid[i][j] == 0:
                for value in range(1, 10):
                    if inferenceOnAvailablePossibleAssignments(i, j, sudokuGrid, setOfCells):
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

setOfCells = {cell: cage for cage in cages for cell in cage['cells']}

callBacktrack()