import pulp


N = 9


class KillerSudokuSolver:

    def __init__(self, cagesList):

        self.cageConstraints = cagesList
        self.sudokuProblem = pulp.LpProblem("Killer Sudoku Problem")
        self.performableChoices = pulp.LpVariable.dicts(
            "Choice", (range(N), range(N), range(1, 10),), cat="Binary"
        )
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
    # not duplicated
    def applyConstraintsOnSudokuGrid(self):

        self.sudokuProblem += (0, "Arbitrary Objective Function")

        # Define the constraint of only one value for each cell
        for i in range(9):
            for j in range(9):
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

        # Each cage has a max total value that has to be the
        # one defined in the problem definition
        for totalSum, cellsList in self.cageConstraints:
            constraintsForCages = [
                self.performableChoices[i][j][n] * n for i, j in cellsList for n in range(1, 10)
            ]
            self.sudokuProblem += pulp.lpSum(constraintsForCages) >= totalSum

    def solve(self):

        self.sudokuProblem.solve()
        if self.sudokuProblem.status != 1:
            raise AssertionError("Problem not sucessfully solved")
        self.parsedResult = [
            [
                int(sum([self.performableChoices[i][j][n].varValue * n for n in range(1, 10)]))
                for j in range(9)
            ]
            for i in range(9)
        ]

        return self.parsedResult


def testSolve():

    # CAGE_CONSTRAINTS = [
    #     (3, [[0, 0], [0, 1]]),
    #     (15, [[0, 2], [0, 3], [0, 4]]),
    #     (22, [[0, 5], [1, 5], [1, 4], [2, 4]]),
    #     (4, [[0, 6], [1, 6]]),
    #     (16, [[0, 7], [1, 7]]),
    #     (15, [[0, 8], [1, 8], [2, 8], [3, 8]]),
    #     (25, [[1, 0], [1, 1], [2, 0], [2, 1]]),
    #     (17, [[1, 2], [1, 3]]),
    #     (9, [[2, 2], [2, 3], [3, 3]]),
    #     (8, [[2, 5], [3, 5], [4, 5]]),
    #     (20, [[2, 6], [2, 7], [3, 6]]),
    #     (6, [[3, 0], [4, 0]]),
    #     (14, [[3, 1], [3, 2]]),
    #     (17, [[3, 4], [4, 4], [5, 4]]),
    #     (17, [[3, 7], [4, 7], [4, 6]]),
    #     (13, [[4, 1], [4, 2], [5, 1]]),
    #     (20, [[4, 3], [5, 3], [6, 3]]),
    #     (12, [[4, 8], [5, 8]]),
    #     (27, [[5, 0], [6, 0], [7, 0], [8, 0]]),
    #     (6, [[5, 2], [6, 2], [6, 1]]),
    #     (20, [[5, 5], [6, 5], [6, 6]]),
    #     (6, [[5, 6], [5, 7]]),
    #     (10, [[6, 4], [7, 4], [7, 3], [8, 3]]),
    #     (14, [[6, 7], [6, 8], [7, 7], [7, 8]]),
    #     (8, [[7, 1], [8, 1]]),
    #     (16, [[7, 2], [8, 2]]),
    #     (15, [[7, 5], [7, 6]]),
    #     (13, [[8, 4], [8, 5], [8, 6]]),
    #     (17, [[8, 7], [8, 8]])
    # ]

    # Define the list of cages as input
    cagesListFile = open("CagesListForMacAlgorithm.txt", "r")
    cagesList = cagesListFile.read()
    cagesList = eval(cagesList)
    print(cagesList)

    killerSolver = KillerSudokuSolver(cagesList=cagesList)

    solution = killerSolver.solve()

    for row in solution:
        print(row)


def main():
    testSolve()


if __name__ == '__main__':
    main()
