# pulp is a library for linear optimization
import pulp
import itertools


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
def applyConstraintsOnSudokuGrid(performableChoices, sudokuProblem, bunchesWithoutDuplicates):
    applyConstraintsOfOneValueForEachCell(performableChoices, sudokuProblem)
    applyConstraintsForCheckingNotDuplicates(performableChoices, sudokuProblem, bunchesWithoutDuplicates)


# Define the constraint of only one value for each cell
def applyConstraintsOfOneValueForEachCell(performableChoices, sudokuProblem):

    for row in range(9):
        for column in range(9):
            constraintOnCellValue = (pulp.lpSum(performableChoices[row][column][value] for value in range(1, 10)) <= 1)
            sudokuProblem = sudokuProblem + constraintOnCellValue


# Works with the dictionary "performableChoices" and
# the total of all bunches without duplicates to update
# the sudoku problem and to ensure that each bunch
# has one occurrence of each number from 1 to 9
def applyConstraintsForCheckingNotDuplicates(performableChoices, sudokuProblem, bunchesWithoutDuplicates):

    for value in range(1, 10):
        for bunch in bunchesWithoutDuplicates:
            for row, column in bunch:
                countCheck = [performableChoices[row][column][value] for row, column in bunch]
                sudokuProblem = sudokuProblem + pulp.lpSum(countCheck) <= 1


# Each cage has a max total value that has to be the
# one defined in the problem definition
def applyConstraintsToTotalValueOfEachCage(performableChoices, sudokuProblem, cagesList):

    for totalSum, cellsList in cagesList:
        for i, j in cellsList:
            for value in range(1, 10):
                constraintsForCages =


def main(cagesList):
    # Define the list of cages as input
    cagesList = cagesList

    # Define the LpProblem with sense minimize
    sudokuProblem = pulp.LpProblem("Killer Sudoku MAC", pulp.constants.LpMinimize)

    # Models a Lp variable with a name (the prefix to the name of each Lp variable created),
    # indexes (a list of strings of the keys to the dictionary of Lp variables),
    # a lower and upper bound on this range of these variables,
    # the category of the variables (in this case Binary)
    performableChoices = pulp.LpVariable.dicts("Choice", (range(9), range(9), range(1, 10)), cat="Binary")

    # Create bunches of rows, columns and subsquares without duplicates
    bunchesWithoutDuplicates = createBunchesWithoutDuplicates()

    sudokuProblem += (0, "The Objective")

    # Apply constraints for sudoku grid
    applyConstraintsOnSudokuGrid(performableChoices, sudokuProblem)
