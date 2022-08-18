import json
import sys


# Defines the cages as tuples starting from json format
from UtilityForAlgorithms import UtilityForAlgorithms


def defineCagesFromJson(json):
    for cage in json:
        cage['cells'] = [tuple(cell) for cell in cage['cells']]
    return json


# Extract all the cells contained in all the cages defined in JSON file and
# checks that each cage doesn't contain duplicated values
def checkCagesNotContainDuplicatedCells(cages):
    cells = [cell for cage in cages for cell in cage['cells']]
    if len(set(cells)) != len(cells):
        raise ValueError('Not valid json, please remove double coordinates before moving forward')


# Add the totalValue values to the 0 grid
def assignTotalValueToCellsOfACage(sudokuGrid, cages):
    for cage in cages:
        for i, j in cage['cells']:
            sudokuGrid[i][j] = cage['totalValue']
    return sudokuGrid


# Checks that there aren't duplicated values in each column
def containsDuplicatedValuesInColumns(sudokuGrid, value, j):
    result = False
    for i in range(0, 9):
        if sudokuGrid[i][j] == value:
            result = True
    return result


# Checks that there aren't duplicated values in each row
def containsDuplicatedValuesInRows(sudokuGrid, value, i):
    result = False
    for j in range(0, 9):
        if sudokuGrid[i][j] == value:
            result = True
    return result


# Checks that there aren't duplicated values in each sub-square 3x3
def containsDuplicatedValuesInSquares(sudokuGrid, value, i, j):
    # Floor division by 3
    i_1 = (i // 3) * 3
    j_1 = (j // 3) * 3
    result = False
    for row in range(0, 3):
        for column in range(0, 3):
            if sudokuGrid[i_1 + row][j_1 + column] == value:
                result = True
    return result


# Checks that all the cells in each cage don't contain 0 elements
def checkBoxesNotContainingZero(cage_elements):
    return 0 not in cage_elements


def inferenceOnPossibleAssignmentsWithFC(i, j, value, sudokuGrid, setOfCells):
    duplicatedValuesInSquares = containsDuplicatedValuesInSquares(sudokuGrid, value, i, j)
    duplicatedValuesInRows = containsDuplicatedValuesInRows(sudokuGrid, value, i)
    duplicatedValuesInColumns = containsDuplicatedValuesInColumns(sudokuGrid, value, j)

    if duplicatedValuesInSquares:
        return False

    if duplicatedValuesInRows:
        return False

    if duplicatedValuesInColumns:
        return False

    currentCage = setOfCells[(i, j)]

    # Cage elements is a list containing the real values
    # initialized with the empty list
    cage_elements = list()

    # If the indexes i,j scanned are also the indexes of a cell contained
    # in the current cage, then add the current value to the
    # cage_elements list, otherwise adds the value stored in the sudoku grid
    # at the indexes i,j
    for row_cell, column_cell in currentCage['cells']:
        if row_cell == i and column_cell == j:
            cage_elements.append(value)
        else:
            cage_elements.append(sudokuGrid[row_cell][column_cell])

    # Sum the values in cage_elements to check that
    # the sum isn't greater than totalValue
    sumToCheck = sum(cage_elements)
    if sumToCheck > currentCage['totalValue']:
        return False

    # Checks that there aren't 0 values in cage_elements
    if checkBoxesNotContainingZero(cage_elements):
        # The sum has to be equal to totalValue
        if currentCage['totalValue'] != sumToCheck:
            return False

        # Checks that the cage_elements list is also a set
        if len(set(cage_elements)) != len(cage_elements):
            return False

    return True


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
        if sudokuGrid[row][
            column] != 0 and row == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages + 1:
            cageAdjacentCells.append([row, column])
        if sudokuGrid[row][
            column] != 0 and row - 1 == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages:
            cageAdjacentCells.append([row, column])
        if sudokuGrid[row][
            column] != 0 and row + 1 == minRowIndexForCellsInCages and column == minColumnIndexForCellsInCages:
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

        isDuplicatedValuesInSquare = containsDuplicatedValuesInSquares(sudokuGrid, value, i, j)
        isDuplicatedValuesInRow = containsDuplicatedValuesInRows(sudokuGrid, value, i)
        isDuplicatedValuesInColumn = containsDuplicatedValuesInColumns(sudokuGrid, value, j)

        if isDuplicatedValuesInSquare and isDuplicatedValuesInRow and isDuplicatedValuesInColumn:
            sudokuGrid[row][column] = value
        else:
            inferenceOnPossibleAssignmentsWithMAC(row, column, value, sudokuGrid, setOfCells)


def callBacktrackFC(sudokuGrid, setOfCells):
    for i in range(9):
        for j in range(9):
            if sudokuGrid[i][j] == 0:
                # "value" is the effective value that we try to put on the current cell
                for value in range(1, 10):
                    if inferenceOnPossibleAssignmentsWithFC(i, j, value, sudokuGrid, setOfCells):
                        sudokuGrid[i][j] = value
                        callBacktrackFC(sudokuGrid, setOfCells)
                        sudokuGrid[i][j] = 0
                return
    UtilityForAlgorithms.printSudokuGrid(sudokuGrid)



def main():
    # From command line specify the .json file
    dataSourceFile = 'SecondTestCagesDataSource.json'  # sys.argv[1]

    # Opening JSON file
    dataSourceJson = open(dataSourceFile)

    # It returns JSON object as a dictionary
    cagesAsDictFromJson = json.load(dataSourceJson)

    cages = defineCagesFromJson(cagesAsDictFromJson)

    # Checks for replicated coordinates in cages
    checkCagesNotContainDuplicatedCells(cages)

    # Initialize grid with all 0
    sudokuGrid = UtilityForAlgorithms.initializeSudokuGrid()

    # Assigns the totalValue to each cell of a cage
    assignTotalValueToCellsOfACage(sudokuGrid, cages)

    sudokuGrid = UtilityForAlgorithms.initializeSudokuGrid()

    # setOfCells is a Dictionary of n x n elements (81):
    # - key = each cell
    # - value = totalValue of the cage to which the cell belongs and
    # the list of all the cells of that cage
    setOfCells = {cell: cage for cage in cages for cell in cage['cells']}

    callBacktrackFC(sudokuGrid, setOfCells)


if __name__ == '__main__':
    main()
