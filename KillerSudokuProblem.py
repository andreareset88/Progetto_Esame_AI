import json
from timeit import default_timer as timer

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


def inferenceOnPossibleAssignmentsWithFC(i, j, value, sudokuGrid, setOfCells, operations):
    duplicatedValuesInSquares = containsDuplicatedValuesInSquares(sudokuGrid, value, i, j)
    duplicatedValuesInRows = containsDuplicatedValuesInRows(sudokuGrid, value, i)
    duplicatedValuesInColumns = containsDuplicatedValuesInColumns(sudokuGrid, value, j)
    operations += 3

    if duplicatedValuesInSquares:
        return False, operations

    if duplicatedValuesInRows:
        return False, operations

    if duplicatedValuesInColumns:
        return False, operations

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
        operations += 1

    # Sum the values in cage_elements to check that
    # the sum isn't greater than totalValue
    sumToCheck = sum(cage_elements)
    if sumToCheck > currentCage['totalValue']:
        operations += 1
        return False, operations

    # Checks that there aren't 0 values in cage_elements
    if checkBoxesNotContainingZero(cage_elements):
        # The sum has to be equal to totalValue
        if currentCage['totalValue'] != sumToCheck:
            operations += 1
            return False, operations

        # Checks that the cage_elements list is also a set
        if len(set(cage_elements)) != len(cage_elements):
            operations += 1
            return False, operations

    return True, operations


def callBacktrackFC(sudokuGrid, setOfCells, operations, totalNumberOfOperations):
    totalNumberOfOperations += operations

    for i in range(9):
        for j in range(9):
            if sudokuGrid[i][j] == 0:
                # "value" is the effective value that we try to put on the current cell
                for value in range(1, 10):
                    result, numOp = inferenceOnPossibleAssignmentsWithFC(i, j, value, sudokuGrid, setOfCells, operations)
                    totalNumberOfOperations += numOp
                    if result:
                        sudokuGrid[i][j] = value
                        operations += 1
                        totalNumberOfOperations += operations
                        print("Partial number of operations: " + str(operations))
                        callBacktrackFC(sudokuGrid, setOfCells, operations, totalNumberOfOperations)
                        sudokuGrid[i][j] = 0
                        operations += 1
                        totalNumberOfOperations += operations
                        print("Partial number of operations: " + str(operations))

                operations += 1
                totalNumberOfOperations += operations
                return None, totalNumberOfOperations
    UtilityForAlgorithms.printSudokuGrid(sudokuGrid)


def main():
    totalTime = 0

    operationsWithFC = 0

    totalOperationsWithFC = 0

    # From command line specify the .json file
    dataSourceFile = 'FirstTestCagesDataSource.json'

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

    for i in range(2):
        start = timer()
        result, numOper = callBacktrackFC(sudokuGrid, setOfCells, operationsWithFC, totalOperationsWithFC)
        end = timer()
        totalTime += end - start

        sudokuGrid = UtilityForAlgorithms.initializeSudokuGrid()
        assignTotalValueToCellsOfACage(sudokuGrid, cages)
        sudokuGrid = UtilityForAlgorithms.initializeSudokuGrid()

    print("Total time with Forward Checking: " + str(totalTime) + " seconds")
    print("\n")
    print("Total operations made by Forward Checking: " + str(numOper))


if __name__ == '__main__':
    main()
