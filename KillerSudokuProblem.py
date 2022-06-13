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
def checkDoubleValuesInColumns(sudokuGrid, value, j):
    for i in range(0, 9):
        if sudokuGrid[i][j] == value:
            return False

# Checks that there aren't duplicated values in each row
def checkDoubleValuesInRows(sudokuGrid, value, i):
    for j in range(0, 9):
        if sudokuGrid[i][j] == value:
            return False

# Checks that there aren't duplicated values in each sub-square 3x3
def checkDoubleValuesInSquares(sudokuGrid, value, i, j):
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

    # Scorri tutte le celle di un cage a partire dalla colonna più a sx e trova
    # gli indici più piccoli delle celle del cage corrente.
    minColumnIndexForCellsInCages = 1
    minRowIndexForCellsInCages = 1
    for row, column in currentCage['cells']:
        if column <= minColumnIndexForCellsInCages and row <= minRowIndexForCellsInCages:
            minRowIndexForCellsInCages = row
            minColumnIndexForCellsInCages = column

    cageAdjacentCells = list()

    # Scandisci tutti gli elementi adiacenti (pur sempre nello stesso cage)
    for row, column in currentCage['cells']:
        # Scorriamo gli elementi nello stesso cage, controllando la colonna adiacente,
        # la riga sotto e la riga sopra
        if sudokuGrid[row][column] != 0 and row == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages + 1:
            cageAdjacentCells.append([row, column])
        if sudokuGrid[row][column] != 0 and row - 1 == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages:
            cageAdjacentCells.append([row, column])
        if sudokuGrid[row][column] != 0 and row + 1 == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages:
            cageAdjacentCells.append([row, column])

    # Occorre controllare, prima di inserire il valore, che esso rispetti i vincoli
    # imposti sulla griglia







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