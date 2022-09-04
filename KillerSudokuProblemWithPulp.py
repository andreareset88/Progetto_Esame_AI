import pulp
from timeit import default_timer as timer


N = 9


class KillerSudokuSolver:

    def __init__(self, cagesList):

        self.operations = 0
        self.cageConstraints = cagesList

        # Define the problem and the sense (Minimize is the default value)
        self.sudokuProblem = pulp.LpProblem("Killer Sudoku Problem")
        self.operations += 1

        # Creates a dictionary of LpVariables with the correct range of values;
        # "range(N)" indicates N (=9) rows and N columns, "range(1,10)" is the
        # range [1,9] for all the values
        self.performableChoices = pulp.LpVariable.dicts(
            "Choice", (range(N), range(N), range(1, 10),), cat="Binary"
        )
        self.operations += 1
        self.bunchesWithoutDuplicates = self.createBunchesWithoutDuplicates()
        self.applyConstraintsOnSudokuGrid()

    # Create bunches of values that don't contain duplicated values
    def createBunchesWithoutDuplicates(self):

        # List the cells for rows
        bunchesOfRows = [[(i, j) for i in range(N)] for j in range(N)]

        # List the cells for columns
        bunchesOfColumns = [[(j, i) for i in range(N)] for j in range(N)]

        # List the sub - squares contained in the original grid
        bunchesOfBoxes = [
            [((3 * i) + k, (3 * j) + l) for k in range(3) for l in range(3)]
            for i in range(3)
            for j in range(3)
        ]

        return bunchesOfRows + bunchesOfColumns + bunchesOfBoxes

    # Apply constraints on sudoku grid ensuring main constraints of the problem:
    # each cell contains one value, each sub - square contains values from 1 to 9
    # not duplicated, and each cage must sum equal to its default value
    # WE DON'T USE THE "==" OPERATOR FOR THE CONSTRAINTS,
    # BECAUSE IT DOESN'T WORK WITH IT, WEIRD!
    def applyConstraintsOnSudokuGrid(self):

        # Set the objective function to 0, because sudoku doesn't need to minimize
        # or maximize it
        self.sudokuProblem += (0, "Arbitrary Objective Function")
        self.operations += 1

        # Define the constraint of only one value for each cell
        for i in range(9):
            for j in range(9):

                # With lpSum, we sum the number of values for each cell, and
                # then we check that each cell contains at most one value
                constraintOnCellValue = (
                        pulp.lpSum([self.performableChoices[i][j][n] for n in range(1, 10)]) <= 1
                )
                self.sudokuProblem += constraintOnCellValue

        # Works with the dictionary "performableChoices" and
        # the total of all bunches without duplicates to update
        # the sudoku problem and to ensure that each bunch
        # has one occurrence of each number from 1 to 9
        for n in range(1, 10):
            for bunch in self.bunchesWithoutDuplicates:
                for i, j in bunch:
                    countCheck = [
                        self.performableChoices[i][j][n] for i, j in bunch
                    ]
                self.sudokuProblem += pulp.lpSum(countCheck) <= 1
            self.operations += 1

        # Each cage has a max total value that has to be the
        # one defined in the problem definition
        for totalSum, cellsList in self.cageConstraints:
            constraintsForCages = [
                self.performableChoices[i][j][n] * n for i, j in cellsList for n in range(1, 10)
            ]

            # Each cage must sum at least totalSum
            self.sudokuProblem += pulp.lpSum(constraintsForCages) >= totalSum
            self.operations += 1

    def solve(self):

        self.sudokuProblem.solve()
        self.operations += 1
        if self.sudokuProblem.status != 1:
            raise AssertionError("Problem not successfully solved")

        # "parsedResult" is how we show the solution, that is a list of
        # values for each row of the grid
        self.parsedResult = [
            [
                int(sum([self.performableChoices[i][j][value].varValue * value for value in range(1, 10)]))
                for j in range(9)
            ]
            for i in range(9)
        ]

        return self.parsedResult


def testSolve():

    # Define the list of cages as input
    cagesListFile = open("CSPLibTestCagesDataSource.txt", "r")
    cagesList = cagesListFile.read()
    cagesList = eval(cagesList)
    print(cagesList)

    killerSolver = KillerSudokuSolver(cagesList=cagesList)

    totalTime = 0
    numOfOperations = 0

    for i in range(50):
        start = timer()
        solution = killerSolver.solve()
        numOfOperations += killerSolver.operations
        end = timer()
        totalTime += end - start
        for row in solution:
            print(row)

    print("\n")
    print("Total execution time: " + str(totalTime) + " seconds")

    print("Number of operations: " + str(numOfOperations))








if __name__ == '__main__':
    testSolve()
