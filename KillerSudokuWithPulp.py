# pulp is a library for linear optimization
import pulp
import itertools


class KillerSudokuWithPulp:

    def __init__(self, cagesList):
        # Define the list of cages as input
        self.cagesList = cagesList

        # Define the LpProblem with sense minimize
        self.sudokuProblem = pulp.LpProblem("Killer Sudoku MAC", pulp.constants.LpMinimize)

        # Models a Lp variable with a name (the prefix to the name of each Lp variable created),
        # indexes (a list of strings of the keys to the dictionary of Lp variables),
        # a lower and upper bound on this range of these variables,
        # the category of the variables (in this case Binary)
        self.performableChoices = pulp.LpVariable.dicts("Choice", (range(9), range(9), range(1, 10)), cat="Binary")
        self.bunchesWithoutDuplicates = self.createBunchesWithoutDuplicates()

    # Create bunches of values that don't contain duplicated values
    def createBunchesWithoutDuplicates(self):

        # List the cells for rows
        bunchesOfRows = [[(row, column) for column in range(9)] for row in range(9)]

        # List the cells for columns
        bunchesOfColumns = [[(row, column) for row in range(9)] for column in range(9)]

        # List the sub - squares contained in the original grid
        bunchesOfBoxes = [
            [((row * 3) + i, (column * 3) + j) for i in range(3) for j in range(3)]
            for row in range(3)
            for column in range(3)
        ]

        # resultOfConcatenation = [*bunchesOfRows, *bunchesOfColumns, *bunchesOfBoxes]

        # bunchesOfRows.extend(bunchesOfColumns)
        # bunchesOfRows.extend(bunchesOfBoxes)

        resultOfConcatenation = itertools.chain(bunchesOfRows, bunchesOfColumns, bunchesOfBoxes)

        return resultOfConcatenation

    # Apply constraints on sudoku grid ensuring main constraints of the problem:
    # each cell contains one value, each subsquare contains values from 1 to 9
    # not duplicated
    def applyConstraintsOnSudokuGrid(self):

        for value in range(1, 10):
            for row in range(9):
                for column in range(9):
                    valueForCell = (pulp.lpSum(self.performableChoices[row][column][value]))

def main():
    list = [[(row, column) for row in range(9)] for column in range(9)]
    print(list)
