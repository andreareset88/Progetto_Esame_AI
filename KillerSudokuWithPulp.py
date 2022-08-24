# pulp is a library for linear optimization
import numpy as np
import pulp, itertools, sys
from UtilityForAlgorithms import UtilityForAlgorithms


# Create bunches of values that don't contain duplicated values
def createBunchesWithoutDuplicates():
    bunchesOfRows = createBunchesOfRows()
    bunchesOfColumns = createBunchesOfColumns()
    bunchesOfBoxes = createBunchesOfBoxes()

    resultOfConcatenation = itertools.chain(bunchesOfRows, bunchesOfColumns, bunchesOfBoxes)

    return resultOfConcatenation


# List the cells for rows
def createBunchesOfRows():
    bunchesOfRows = [[(row, column) for column in range(9)] for row in range(9)]
    return bunchesOfRows


# List the cells for columns
def createBunchesOfColumns():
    bunchesOfColumns = [[(row, column) for row in range(9)] for column in range(9)]
    return bunchesOfColumns


# List the sub - squares contained in the original grid
def createBunchesOfBoxes():
    bunchesOfBoxes = [
        [((3 * row) + i, (3 * column) + j) for i in range(3) for j in range(3)]
        for row in range(3)
        for column in range(3)
    ]

    return bunchesOfBoxes


# Apply constraints on sudoku grid ensuring main constraints of the problem:
# each cell contains one value, each subsquare contains values from 1 to 9
# not duplicated
def applyConstraintsOnSudokuGrid(performableChoices, sudokuProblem, bunchesWithoutDuplicates, cagesList):
    sudokuProblem = applyConstraintsOfOneValueForEachCell(performableChoices, sudokuProblem)
    sudokuProblem = applyConstraintsForCheckingNotDuplicates(performableChoices, sudokuProblem, bunchesWithoutDuplicates)
    sudokuProblem = applyConstraintsToTotalValueOfEachCage(performableChoices, sudokuProblem, cagesList)

    return sudokuProblem


# Define the constraint of only one value for each cell
def applyConstraintsOfOneValueForEachCell(performableChoices, sudokuProblem):
    for row in range(9):
        for column in range(9):
            constraintOnCellValue = (pulp.lpSum(performableChoices[row][column][value] for value in range(1, 10)) <= 1)
            sudokuProblem += constraintOnCellValue

    return sudokuProblem


# Works with the dictionary "performableChoices" and
# the total of all bunches without duplicates to update
# the sudoku problem and to ensure that each bunch
# has one occurrence of each number from 1 to 9
def applyConstraintsForCheckingNotDuplicates(performableChoices, sudokuProblem, bunchesWithoutDuplicates):
    for value in range(1, 10):
        for bunch in bunchesWithoutDuplicates:
            for row, column in bunch:
                countCheck = [performableChoices[row][column][value] for row, column in bunch]
                sudokuProblem += pulp.lpSum(countCheck) <= 1

    return sudokuProblem


# Each cage has a max total value that has to be the
# one defined in the problem definition
def applyConstraintsToTotalValueOfEachCage(performableChoices, sudokuProblem, cagesList):
    for totalSum, cellsList in cagesList:
        constraintsForCages = [
            performableChoices[row][column][value] * value
            for row, column in cellsList
            for value in range(1, 10)]
        sudokuProblem += pulp.lpSum(constraintsForCages) >= totalSum

    return sudokuProblem


def main():
    # Define the list of cages as input
    cagesListFile = open("CagesListForMacAlgorithm.txt", "r")
    cagesList = cagesListFile.read()
    cagesList = eval(cagesList)
    print(cagesList)

    # cagesList = [
    #     (8, [[0, 0], [0, 1]]),
    #     (9, [[0, 6], [0, 7]]),
    #     (8, [[0, 2], [1, 2]]),
    #     (12, [[0, 3], [0, 4], [1, 3]]),
    #     (15, [[0, 5], [1, 5], [2, 5]]),
    #     (19, [[1, 6], [1, 7], [2, 7]]),
    #     (16, [[0, 8], [1, 8], [2, 8]]),
    #     (14, [[1, 0], [1, 1], [2, 0]]),
    #     (15, [[2, 1], [2, 2]]),
    #     (10, [[2, 3], [3, 3]]),
    #     (12, [[1, 4], [2, 4]]),
    #     (7, [[2, 6], [3, 6]]),
    #     (24, [[3, 0], [3, 1], [4, 1]]),
    #     (17, [[3, 7], [3, 8], [4, 8]]),
    #     (8, [[3, 2], [4, 2]]),
    #     (12, [[4, 3], [5, 3]]),
    #     (19, [[3, 4], [4, 4], [5, 4]]),
    #     (4, [[3, 5], [4, 5]]),
    #     (15, [[4, 6], [5, 6]]),
    #     (12, [[4, 0], [5, 0], [5, 1]]),
    #     (7, [[4, 7], [5, 7], [5, 8]]),
    #     (8, [[5, 2], [6, 2]]),
    #     (10, [[6, 4], [7, 4]]),
    #     (14, [[5, 5], [6, 5]]),
    #     (12, [[6, 6], [6, 7]]),
    #     (18, [[6, 8], [7, 7], [7, 8]]),
    #     (15, [[6, 0], [7, 0], [8, 0]]),
    #     (13, [[6, 1], [7, 1], [7, 2]]),
    #     (12, [[6, 3], [7, 3], [8, 3]]),
    #     (15, [[7, 5], [8, 4], [8, 5]]),
    #     (7, [[7, 6], [8, 6]]),
    #     (10, [[8, 1], [8, 2]]),
    #     (8, [[8, 7], [8, 8]])
    # ]

    # Define the LpProblem with sense minimize
    sudokuProblem = pulp.LpProblem("Killer Sudoku Problem")

    # Models a Lp variable with a name (the prefix to the name of each Lp variable created),
    # indexes (a list of strings of the keys to the dictionary of Lp variables),
    # a lower and upper bound on this range of these variables,
    # the category of the variables (in this case Binary)
    performableChoices = pulp.LpVariable.dicts("Choice", (range(9), range(9), range(1, 10)), cat="Binary")

    # Create bunches of rows, columns and subsquares without duplicates
    bunchesWithoutDuplicates = createBunchesWithoutDuplicates()

    sudokuProblem += (0, "The Objective Function")

    # Apply constraints for sudoku grid
    sudokuProblem = applyConstraintsOnSudokuGrid(performableChoices, sudokuProblem, bunchesWithoutDuplicates, cagesList)

    sudokuProblem.solve()

    if sudokuProblem.status != 1:
        print("Error!", file=sys.stderr)
        raise SystemExit(1)

    # varValue is a pulp function that permits to have the best optimization for the variables
    # of the problem
    sudokuSolution = [
        [
          int([performableChoices[row][column][value].varValue * value for value in range(1, 10)])
          for column in range(9)
        ]
        for row in range(9)

    ]

    # assert sudokuSolution[8][7] + sudokuSolution[8][8] == 8
    # assert sudokuSolution[0][0] + sudokuSolution[0][1] == 8
    # assert sudokuSolution[6][8] + sudokuSolution[7][7] + sudokuSolution[7][8] == 18
    # assert sudokuSolution[3][2] + sudokuSolution[4][2] == 8

    solution = np.array(sudokuSolution)

    print(solution)

    # Assert that the sum of all the values in each row and column is 45,
    # that corresponds to the result of 1+2+3+4+5+6+7+8+9
    assert(solution.sum(axis=1) == 45).all()

    assert (solution.sum(axis=0) == 45).all()

    UtilityForAlgorithms.printSudokuGrid(solution)


if __name__ == '__main__':
    main()
